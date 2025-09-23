"""
Main recommendation engine that orchestrates the entire recommendation process.

This module provides the primary RecommendationEngine class that coordinates
filtering, scoring, and categorization to generate career recommendations.
"""

from typing import List, Dict, Optional
import logging
import json
from ..models import UserProfileModel as UserProfile, CareerModel as Career, SkillModel as Skill, RecommendationModel as CareerRecommendation
from .config import RecommendationConfig, DEFAULT_CONFIG
from .filters import FilterEngine
from .scoring import ScoringEngine
from .categorization import CategorizationEngine
from .career_database import normalize_career_title

# Set up logging
logger = logging.getLogger(__name__)

# Constants for prompt size validation
MAX_PROMPT_SIZE = 100000  # Maximum characters in prompt (adjust based on model limits)
MAX_CAREERS_FOR_PROMPT = 50  # Maximum number of careers to include in a single prompt


class RecommendationEngine:
    """
    Main recommendation engine that orchestrates the entire process.
    
    This class coordinates:
    1. Multi-stage filtering of careers
    2. Weighted scoring of filtered careers
    3. Categorization into Safe/Stretch/Adventure zones
    4. Generation of explanations and reasons
    """
    
    def __init__(
        self, 
        config: Optional[RecommendationConfig] = None,
        skills_db: Optional[List[Skill]] = None
    ):
        """
        Initialize the recommendation engine.
        
        Args:
            config: Configuration for the recommendation engine
            skills_db: Database of all available skills
        """
        self.config = config or DEFAULT_CONFIG
        self.skills_db = skills_db or []
        
        # Initialize component engines
        self.filter_engine = FilterEngine(self.config.filtering_config, self.skills_db)
        self.scoring_engine = ScoringEngine(
            self.config.scoring_config,
            self.config.scoring_weights,
            self.config.consistency_penalty_config
        )
        self.categorization_engine = CategorizationEngine(
            self.config.categorization_thresholds
        )
    
    def get_recommendations(
        self,
        user_profile: UserProfile,
        available_careers: List[Career],
        limit: Optional[int] = None,
        exploration_level: int = 3
    ) -> List[CareerRecommendation]:
        """
        Generate career recommendations for a user using the new multi-step process.
        
        This method implements the new architecture to prevent "prompt too long" errors:
        1. Pre-process user profile to create a concise summary
        2. Pre-filter careers using lightweight, non-LLM filtering
        3. Use multi-call recommendation generation with smaller batches
        
        Args:
            user_profile: User's profile with skills, interests, and preferences
            available_careers: List of all available careers to consider
            limit: Maximum number of recommendations to return
            exploration_level: User's exploration level (1-5) for consistency penalty
            
        Returns:
            List of CareerRecommendation objects sorted by score
        """
        logger.info(f"Starting recommendation generation for user with {len(available_careers)} available careers")
        
        # Step 1: Pre-process the user profile to create a concise summary
        summarized_profile = self._preprocess_user_profile(user_profile)
        
        # Step 2: Pre-filter careers using lightweight filtering
        candidate_careers = self._prefilter_careers(summarized_profile, available_careers)
        
        if not candidate_careers:
            # If pre-filtering returns no results, fall back to traditional filtering
            logger.warning("Pre-filtering returned no careers, falling back to traditional filtering")
            candidate_careers = self.filter_engine.filter_careers(user_profile, available_careers)
            
            if not candidate_careers:
                # If still no careers, use fallback filtering
                candidate_careers = self._fallback_filtering(user_profile, available_careers)
        
        # Step 3: Validate prompt size and truncate if necessary
        validated_careers, was_truncated = self._validate_prompt_size(user_profile, candidate_careers)
        
        if was_truncated:
            logger.warning(f"Career list was truncated from {len(candidate_careers)} to {len(validated_careers)} to prevent prompt overflow")
        
        # Step 4: Multi-call recommendation generation
        # Apply traditional filtering to the validated careers for additional refinement
        refined_careers = self.filter_engine.filter_careers(user_profile, validated_careers)
        
        if not refined_careers:
            # If refined filtering removes all careers, use the validated list
            refined_careers = validated_careers
        
        logger.info(f"Using {len(refined_careers)} careers for final scoring and categorization")
        
        # Step 5: Score the refined careers with consistency penalty
        scores = self.scoring_engine.score_multiple_careers(user_profile, refined_careers, exploration_level)
        
        # Step 6: Categorize recommendations
        recommendations = self.categorization_engine.categorize_recommendations(
            user_profile, refined_careers, scores
        )
        
        # Step 7: Apply final limits and sorting
        recommendations.sort(key=lambda x: x.score.total_score, reverse=True)
        
        if limit:
            recommendations = recommendations[:limit]
        elif len(recommendations) > self.config.max_recommendations:
            recommendations = recommendations[:self.config.max_recommendations]
        
        # Ensure minimum recommendations if possible
        if len(recommendations) < self.config.min_recommendations and len(available_careers) >= self.config.min_recommendations:
            recommendations = self._ensure_minimum_recommendations(
                user_profile, available_careers, recommendations, exploration_level
            )
        
        logger.info(f"Generated {len(recommendations)} final recommendations")
        
        return recommendations
    
    def get_recommendations_by_category(
        self,
        user_profile: UserProfile,
        available_careers: List[Career],
        limit_per_category: int = 5,
        exploration_level: int = 3
    ) -> Dict[str, List[CareerRecommendation]]:
        """
        Get recommendations organized by category.
        
        Args:
            user_profile: User's profile
            available_careers: List of available careers
            limit_per_category: Maximum recommendations per category
            exploration_level: User's exploration level (1-5)
            
        Returns:
            Dictionary with recommendations organized by category
        """
        all_recommendations = self.get_recommendations(user_profile, available_careers, None, exploration_level)
        
        return self.categorization_engine.get_top_recommendations_per_category(
            all_recommendations, limit_per_category
        )
    
    def explain_recommendation(
        self,
        user_profile: UserProfile,
        career: Career,
        exploration_level: int = 3
    ) -> Dict[str, any]:
        """
        Generate detailed explanation for why a career was recommended.
        
        Args:
            user_profile: User's profile
            career: Career to explain
            exploration_level: User's exploration level (1-5)
            
        Returns:
            Dictionary with detailed explanation
        """
        # Score the individual career
        score = self.scoring_engine.score_career(user_profile, career, exploration_level)
        
        # Categorize it
        recommendations = self.categorization_engine.categorize_recommendations(
            user_profile, [career], [score]
        )
        
        if not recommendations:
            return {"error": "Could not generate explanation"}
        
        recommendation = recommendations[0]
        
        return {
            "career_title": career.title,
            "total_score": score.total_score,
            "category": recommendation.category.value,
            "confidence": recommendation.confidence,
            "reasons": recommendation.reasons,
            "score_breakdown": {
                "skill_match": score.skill_match_score,
                "interest_match": score.interest_match_score,
                "salary_compatibility": score.salary_compatibility_score,
                "experience_match": score.experience_match_score,
                "consistency_penalty": score.consistency_penalty
            },
            "detailed_breakdown": score.breakdown
        }
    
    def get_recommendation_statistics(
        self,
        user_profile: UserProfile,
        available_careers: List[Career],
        exploration_level: int = 3
    ) -> Dict[str, any]:
        """
        Get statistics about the recommendation process.
        
        Args:
            user_profile: User's profile
            available_careers: List of available careers
            exploration_level: User's exploration level (1-5)
            
        Returns:
            Dictionary with recommendation statistics
        """
        # Get filtering statistics
        filter_stats = self.filter_engine.get_filter_statistics(user_profile, available_careers)
        
        # Get recommendations
        recommendations = self.get_recommendations(user_profile, available_careers, None, exploration_level)
        
        # Get category distribution
        category_distribution = self.categorization_engine.get_category_distribution(recommendations)
        
        # Calculate score statistics
        if recommendations:
            scores = [rec.score.total_score for rec in recommendations]
            penalties = [rec.score.consistency_penalty for rec in recommendations]
            score_stats = {
                "average_score": sum(scores) / len(scores),
                "highest_score": max(scores),
                "lowest_score": min(scores),
                "score_range": max(scores) - min(scores),
                "average_consistency_penalty": sum(penalties) / len(penalties),
                "max_consistency_penalty": max(penalties)
            }
        else:
            score_stats = {
                "average_score": 0.0,
                "highest_score": 0.0,
                "lowest_score": 0.0,
                "score_range": 0.0,
                "average_consistency_penalty": 0.0,
                "max_consistency_penalty": 0.0
            }
        
        return {
            "filtering_stats": filter_stats,
            "category_distribution": category_distribution,
            "score_statistics": score_stats,
            "total_recommendations": len(recommendations),
            "configuration": {
                "max_recommendations": self.config.max_recommendations,
                "min_recommendations": self.config.min_recommendations,
                "scoring_weights": {
                    "skill_match": self.config.scoring_weights.skill_match,
                    "interest_match": self.config.scoring_weights.interest_match,
                    "salary_compatibility": self.config.scoring_weights.salary_compatibility,
                    "experience_match": self.config.scoring_weights.experience_match
                },
                "consistency_penalty": {
                    "base_penalty": self.config.consistency_penalty_config.base_penalty,
                    "exploration_multiplier": self.config.consistency_penalty_config.exploration_level_multiplier.get(exploration_level, 1.0),
                    "max_penalty": self.config.consistency_penalty_config.max_penalty
                }
            }
        }
    
    def _fallback_filtering(
        self, 
        user_profile: UserProfile, 
        available_careers: List[Career]
    ) -> List[Career]:
        """
        Fallback filtering when initial filtering returns no results.
        
        Args:
            user_profile: User's profile
            available_careers: List of all careers
            
        Returns:
            List of careers with relaxed filtering
        """
        # Try with relaxed salary constraints
        relaxed_careers = self.filter_engine.apply_initial_filters(user_profile, available_careers)
        
        if relaxed_careers:
            return relaxed_careers
        
        # If still no results, return top careers by basic compatibility
        return available_careers[:self.config.max_recommendations]
    
    def _ensure_minimum_recommendations(
        self,
        user_profile: UserProfile,
        available_careers: List[Career],
        current_recommendations: List[CareerRecommendation],
        exploration_level: int = 3
    ) -> List[CareerRecommendation]:
        """
        Ensure minimum number of recommendations by adding lower-scored options.
        
        Args:
            user_profile: User's profile
            available_careers: All available careers
            current_recommendations: Current recommendations
            exploration_level: User's exploration level (1-5)
            
        Returns:
            Extended list of recommendations
        """
        if len(current_recommendations) >= self.config.min_recommendations:
            return current_recommendations
        
        # Get careers not already recommended
        recommended_ids = {rec.career.career_id for rec in current_recommendations}
        remaining_careers = [
            career for career in available_careers
            if career.career_id not in recommended_ids
        ]
        
        # Score remaining careers
        remaining_scores = self.scoring_engine.score_multiple_careers(
            user_profile, remaining_careers, exploration_level
        )
        
        # Categorize additional recommendations
        additional_recommendations = self.categorization_engine.categorize_recommendations(
            user_profile, remaining_careers, remaining_scores
        )
        
        # Add best additional recommendations
        needed = self.config.min_recommendations - len(current_recommendations)
        additional_recommendations.sort(key=lambda x: x.score.total_score, reverse=True)
        
        return current_recommendations + additional_recommendations[:needed]
    
    def update_config(self, new_config: RecommendationConfig):
        """
        Update the engine configuration.
        
        Args:
            new_config: New configuration to apply
        """
        self.config = new_config
        
        # Reinitialize component engines with new config
        self.filter_engine = FilterEngine(self.config.filtering_config, self.skills_db)
        self.scoring_engine = ScoringEngine(
            self.config.scoring_config,
            self.config.scoring_weights,
            self.config.consistency_penalty_config
        )
        self.categorization_engine = CategorizationEngine(
            self.config.categorization_thresholds
        )
    
    def update_skills_database(self, skills_db: List[Skill]):
        """
        Update the skills database.
        
        Args:
            skills_db: New skills database
        """
        self.skills_db = skills_db
        self.filter_engine = FilterEngine(self.config.filtering_config, self.skills_db)
    
    def _preprocess_user_profile(self, user_profile: UserProfile) -> Dict:
        """
        Summarizes the user's profile and resume using a dedicated process.
        
        This method condenses the user's profile into a concise summary to reduce
        the amount of data sent in subsequent steps, preventing "prompt too long" errors.
        
        Args:
            user_profile: The user's full profile.
            
        Returns:
            A dictionary containing the summarized profile.
        """
        logger.info("Starting user profile preprocessing")
        
        # Extract key information from the user profile
        summary = {
            "key_skills": user_profile.technicalSkills[:10] if user_profile.technicalSkills else [],
            "soft_skills": user_profile.softSkills[:5] if user_profile.softSkills else [],
            "experience_years": user_profile.experience,
            "primary_industries": user_profile.industries[:3] if user_profile.industries else [],
            "career_goals": user_profile.careerGoals,
            "interests": user_profile.interests[:5] if user_profile.interests else [],
            "work_preferences": {
                "workingWithData": getattr(user_profile, 'workingWithData', 3),
                "workingWithPeople": getattr(user_profile, 'workingWithPeople', 3),
                "creativeTasks": getattr(user_profile, 'creativeTasks', 3),
                "problemSolving": getattr(user_profile, 'problemSolving', 3),
                "leadership": getattr(user_profile, 'leadership', 3),
                "physicalHandsOnWork": getattr(user_profile, 'physicalHandsOnWork', 3),
                "mechanicalAptitude": getattr(user_profile, 'mechanicalAptitude', 3)
            },
            "salary_range": user_profile.salaryExpectations,
            "education_level": user_profile.educationLevel,
            "current_role": user_profile.currentRole,
            "location": user_profile.location
        }
        
        # Summarize resume text if it's too long (keep first 500 characters)
        if hasattr(user_profile, 'resumeText') and user_profile.resumeText:
            resume_text = user_profile.resumeText.strip()
            if len(resume_text) > 500:
                summary["resume_summary"] = resume_text[:500] + "..."
            else:
                summary["resume_summary"] = resume_text
        else:
            summary["resume_summary"] = ""
        
        logger.info(f"User profile preprocessed: {len(summary['key_skills'])} skills, "
                   f"{len(summary['primary_industries'])} industries")
        
        return summary
    
    def _prefilter_careers(
        self,
        summarized_profile: Dict,
        available_careers: List[Career],
    ) -> List[Career]:
        """
        Prefilters the list of available careers based on the summarized profile.
        
        This method implements lightweight, non-LLM filtering to reduce the career
        dataset before the more expensive scoring phase.
        
        Args:
            summarized_profile: The summarized user profile.
            available_careers: The full list of available careers.
            
        Returns:
            A filtered list of candidate careers.
        """
        logger.info(f"Starting career pre-filtering from {len(available_careers)} careers")
        
        # Extract key filtering criteria
        user_skills = set(skill.lower() for skill in summarized_profile.get("key_skills", []))
        user_industries = set(industry.lower() for industry in summarized_profile.get("primary_industries", []))
        user_interests = set(interest.lower() for interest in summarized_profile.get("interests", []))
        
        # Score each career for relevance
        career_scores = []
        
        for career in available_careers:
            score = 0.0
            
            # Skill matching (40% weight)
            career_skills = set()
            if hasattr(career, 'requiredSkills') and career.requiredSkills:
                career_skills.update(skill.lower() for skill in career.requiredSkills)
            if hasattr(career, 'preferredSkills') and career.preferredSkills:
                career_skills.update(skill.lower() for skill in career.preferredSkills)
            
            if career_skills and user_skills:
                skill_overlap = len(user_skills.intersection(career_skills))
                skill_score = skill_overlap / max(len(user_skills), len(career_skills))
                score += skill_score * 0.4
            
            # Industry matching (30% weight)
            career_industries = set()
            if hasattr(career, 'industry') and career.industry:
                career_industries.add(career.industry.lower())
            if hasattr(career, 'industries') and career.industries:
                career_industries.update(industry.lower() for industry in career.industries)
            
            if career_industries and user_industries:
                industry_overlap = len(user_industries.intersection(career_industries))
                industry_score = industry_overlap / len(user_industries)
                score += industry_score * 0.3
            
            # Interest/keyword matching (20% weight)
            career_text = f"{normalize_career_title(career.title)} {getattr(career, 'description', '')}".lower()
            interest_matches = sum(1 for interest in user_interests if interest in career_text)
            if user_interests:
                interest_score = interest_matches / len(user_interests)
                score += interest_score * 0.2
            
            # Title relevance (10% weight)
            title_matches = sum(1 for skill in user_skills if skill in normalize_career_title(career.title))
            if user_skills:
                title_score = min(title_matches / len(user_skills), 1.0)
                score += title_score * 0.1
            
            career_scores.append((career, score))
        
        # Sort by score and take top candidates
        career_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Take top N careers based on configuration
        max_careers = min(self.config.prefilter_limit, len(career_scores))
        filtered_careers = [career for career, score in career_scores[:max_careers]]
        
        logger.info(f"Pre-filtering completed: {len(filtered_careers)} careers selected from {len(available_careers)}")
        
        return filtered_careers
    
    def _validate_prompt_size(
        self,
        user_profile: UserProfile,
        careers: List[Career],
        max_size: int = MAX_PROMPT_SIZE
    ) -> tuple[List[Career], bool]:
        """
        Validate that the prompt size is within acceptable limits.
        
        This method estimates the size of the prompt that would be sent to the model
        and truncates the career list if necessary to prevent "prompt too long" errors.
        
        Args:
            user_profile: User's profile
            careers: List of careers to include in prompt
            max_size: Maximum allowed prompt size in characters
            
        Returns:
            Tuple of (truncated_careers_list, was_truncated)
        """
        logger.info(f"Validating prompt size for {len(careers)} careers")
        
        # Estimate prompt size by serializing key data
        try:
            # Create a simplified representation of the data that would be in the prompt
            prompt_data = {
                "user_profile": {
                    "skills": [skill.name for skill in user_profile.skills],
                    "interests": list(user_profile.assessment_results.interests.keys()),
                    "experience_years": sum(exp.duration_years for exp in user_profile.professional_data.experience),
                    "salary_range": user_profile.personal_info.salary_expectations.dict() if user_profile.personal_info.salary_expectations else None,
                    "work_values": user_profile.assessment_results.work_values,
                    "personality_traits": user_profile.assessment_results.personality_traits
                },
                "careers": [
                    {
                        "title": career.title,
                        "description": career.description[:200],  # Truncate description for estimation
                        "required_skills": [skill.name for skill in career.required_skills],
                        "salary_range": career.salary_range.dict(),
                        "career_field": career.career_field
                    }
                    for career in careers
                ]
            }
            
            # Estimate prompt size
            estimated_size = len(json.dumps(prompt_data, default=str))
            logger.info(f"Estimated prompt size: {estimated_size} characters")
            
            if estimated_size <= max_size:
                return careers, False
            
            # If prompt is too large, truncate careers list
            logger.warning(f"Prompt size ({estimated_size}) exceeds limit ({max_size}). Truncating careers list.")
            
            # Binary search to find maximum number of careers that fit
            left, right = 1, len(careers)
            best_count = min(MAX_CAREERS_FOR_PROMPT, len(careers))
            
            while left <= right:
                mid = (left + right) // 2
                test_careers = careers[:mid]
                
                test_data = prompt_data.copy()
                test_data["careers"] = [
                    {
                        "title": career.title,
                        "description": career.description[:200],
                        "required_skills": [skill.name for skill in career.required_skills],
                        "salary_range": career.salary_range.dict(),
                        "career_field": career.career_field
                    }
                    for career in test_careers
                ]
                
                test_size = len(json.dumps(test_data, default=str))
                
                if test_size <= max_size:
                    best_count = mid
                    left = mid + 1
                else:
                    right = mid - 1
            
            truncated_careers = careers[:best_count]
            logger.warning(f"Truncated careers list from {len(careers)} to {len(truncated_careers)} careers")
            
            return truncated_careers, True
            
        except Exception as e:
            logger.error(f"Error during prompt size validation: {e}")
            # Fallback: use a conservative limit
            fallback_limit = min(MAX_CAREERS_FOR_PROMPT, len(careers))
            logger.warning(f"Using fallback limit of {fallback_limit} careers due to validation error")
            return careers[:fallback_limit], len(careers) > fallback_limit