"""
Enhanced recommendation engine with improved categorization and accuracy.

This module provides an enhanced RecommendationEngine class that uses the new
context-aware categorization system to address the accuracy issues identified
in the original implementation.
"""

from typing import List, Dict, Optional
import logging
import json
from .config import RecommendationConfig, DEFAULT_CONFIG
from .filters import FilterEngine
from .scoring import ScoringEngine
from .enhanced_categorization import EnhancedCategorizationEngine

# Import models - try both relative and absolute imports
try:
    from ..models import UserProfileModel as UserProfile, CareerModel as Career, SkillModel as Skill, RecommendationModel as CareerRecommendation
except ImportError:
    try:
        from models import UserProfileModel as UserProfile, CareerModel as Career, SkillModel as Skill, RecommendationModel as CareerRecommendation
    except ImportError:
        # Fallback: define basic types if models can't be imported
        from typing import Any
        UserProfile = Any
        Career = Any
        Skill = Any
        CareerRecommendation = Any

# Set up logging
logger = logging.getLogger(__name__)

# Constants for prompt size validation
MAX_PROMPT_SIZE = 100000  # Maximum characters in prompt (adjust based on model limits)
MAX_CAREERS_FOR_PROMPT = 50  # Maximum number of careers to include in a single prompt


class EnhancedRecommendationEngine:
    """
    Enhanced recommendation engine with improved categorization accuracy.
    
    This class addresses the issues identified in the original engine:
    1. Context-aware career field categorization
    2. Seniority-level awareness in recommendations
    3. Better handling of executive-level roles
    4. Improved field transition logic
    """
    
    def __init__(
        self, 
        config: Optional[RecommendationConfig] = None,
        skills_db: Optional[List[Skill]] = None,
        use_enhanced_categorization: bool = True
    ):
        """
        Initialize the enhanced recommendation engine.
        
        Args:
            config: Configuration for the recommendation engine
            skills_db: Database of all available skills
            use_enhanced_categorization: Whether to use enhanced categorization
        """
        self.config = config or DEFAULT_CONFIG
        self.skills_db = skills_db or []
        self.use_enhanced_categorization = use_enhanced_categorization
        
        # Initialize component engines
        self.filter_engine = FilterEngine(self.config.filtering_config, self.skills_db)
        self.scoring_engine = ScoringEngine(
            self.config.scoring_config,
            self.config.scoring_weights,
            self.config.consistency_penalty_config
        )
        
        # Use enhanced or original categorization engine
        if use_enhanced_categorization:
            self.categorization_engine = EnhancedCategorizationEngine(
                self.config.categorization_thresholds
            )
        else:
            from .categorization import CategorizationEngine
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
        Generate career recommendations using enhanced categorization.
        
        Args:
            user_profile: User's profile with skills, interests, and preferences
            available_careers: List of all available careers to consider
            limit: Maximum number of recommendations to return
            exploration_level: User's exploration level (1-5) for consistency penalty
            
        Returns:
            List of CareerRecommendation objects sorted by score with enhanced accuracy
        """
        logger.info(f"Starting enhanced recommendation generation for user with {len(available_careers)} available careers")
        
        # Step 1: Pre-process the user profile
        summarized_profile = self._preprocess_user_profile(user_profile)
        
        # Step 2: Enhanced pre-filtering with field awareness
        candidate_careers = self._enhanced_prefilter_careers(summarized_profile, available_careers, user_profile)
        
        if not candidate_careers:
            logger.warning("Enhanced pre-filtering returned no careers, falling back to traditional filtering")
            candidate_careers = self.filter_engine.filter_careers(user_profile, available_careers)
            
            if not candidate_careers:
                candidate_careers = self._fallback_filtering(user_profile, available_careers)
        
        # Step 3: Validate prompt size
        validated_careers, was_truncated = self._validate_prompt_size(user_profile, candidate_careers)
        
        if was_truncated:
            logger.warning(f"Career list was truncated from {len(candidate_careers)} to {len(validated_careers)} to prevent prompt overflow")
        
        # Step 4: Apply additional filtering
        refined_careers = self.filter_engine.filter_careers(user_profile, validated_careers)
        
        if not refined_careers:
            refined_careers = validated_careers
        
        logger.info(f"Using {len(refined_careers)} careers for enhanced scoring and categorization")
        
        # Step 5: Score careers
        scores = self.scoring_engine.score_multiple_careers(user_profile, refined_careers, exploration_level)
        
        # Step 6: Enhanced categorization
        recommendations = self.categorization_engine.categorize_recommendations(
            user_profile, refined_careers, scores
        )
        
        # Step 7: Apply enhanced sorting and filtering
        recommendations = self._apply_enhanced_sorting(recommendations, user_profile)
        
        if limit:
            recommendations = recommendations[:limit]
        elif len(recommendations) > self.config.max_recommendations:
            recommendations = recommendations[:self.config.max_recommendations]
        
        # Ensure minimum recommendations
        if len(recommendations) < self.config.min_recommendations and len(available_careers) >= self.config.min_recommendations:
            recommendations = self._ensure_minimum_recommendations(
                user_profile, available_careers, recommendations, exploration_level
            )
        
        logger.info(f"Generated {len(recommendations)} enhanced recommendations")
        
        return recommendations
    
    def _enhanced_prefilter_careers(
        self,
        summarized_profile: Dict,
        available_careers: List[Career],
        user_profile: UserProfile
    ) -> List[Career]:
        """
        Enhanced pre-filtering that considers career fields and seniority levels.
        
        Args:
            summarized_profile: Summarized user profile
            available_careers: All available careers
            user_profile: Full user profile for enhanced analysis
            
        Returns:
            Filtered list of candidate careers
        """
        logger.info(f"Starting enhanced career pre-filtering from {len(available_careers)} careers")
        
        # Import enhanced categorization functions
        from .enhanced_categorization import (
            determine_enhanced_user_career_field, 
            get_enhanced_career_field,
            extract_seniority_level,
            ENHANCED_CAREER_FIELD_CATEGORIES
        )
        
        # Determine user's career field and seniority
        user_field, user_field_confidence = determine_enhanced_user_career_field(user_profile)
        user_seniority = self._get_user_seniority_level(user_profile)
        
        logger.info(f"User profile: field={user_field} (confidence={user_field_confidence:.2f}), seniority={user_seniority}")
        
        # Extract filtering criteria
        user_skills = set(skill.lower() for skill in summarized_profile.get("key_skills", []))
        user_industries = set(industry.lower() for industry in summarized_profile.get("primary_industries", []))
        user_interests = set(interest.lower() for interest in summarized_profile.get("interests", []))
        
        # Score each career with enhanced logic
        career_scores = []
        
        for career in available_careers:
            score = 0.0
            
            # Get career field and seniority
            career_field, career_field_confidence = get_enhanced_career_field(career)
            career_seniority = extract_seniority_level(career.title)
            
            # Field alignment scoring (40% weight)
            if user_field == career_field:
                score += 0.4 * user_field_confidence * career_field_confidence
            elif career_field in ENHANCED_CAREER_FIELD_CATEGORIES.get(user_field, type('obj', (object,), {'related_fields': []})).related_fields:
                score += 0.25 * user_field_confidence * career_field_confidence
            else:
                # Penalty for unrelated fields, but not complete exclusion
                score += 0.1 * career_field_confidence
            
            # Seniority alignment scoring (25% weight)
            seniority_levels = ['junior', 'mid', 'senior', 'executive']
            user_seniority_idx = seniority_levels.index(user_seniority) if user_seniority in seniority_levels else 1
            career_seniority_idx = seniority_levels.index(career_seniority) if career_seniority in seniority_levels else 1
            seniority_gap = abs(career_seniority_idx - user_seniority_idx)
            
            if seniority_gap == 0:
                score += 0.25
            elif seniority_gap == 1:
                score += 0.20
            elif seniority_gap == 2:
                score += 0.10
            else:
                score += 0.05
            
            # Skill matching (20% weight)
            career_skills = set()
            if hasattr(career, 'requiredSkills') and career.requiredSkills:
                career_skills.update(skill.lower() for skill in career.requiredSkills)
            if hasattr(career, 'preferredSkills') and career.preferredSkills:
                career_skills.update(skill.lower() for skill in career.preferredSkills)
            
            if career_skills and user_skills:
                skill_overlap = len(user_skills.intersection(career_skills))
                skill_score = skill_overlap / max(len(user_skills), len(career_skills))
                score += skill_score * 0.2
            
            # Industry matching (10% weight)
            career_industries = set()
            if hasattr(career, 'industry') and career.industry:
                career_industries.add(career.industry.lower())
            if hasattr(career, 'industries') and career.industries:
                career_industries.update(industry.lower() for industry in career.industries)
            
            if career_industries and user_industries:
                industry_overlap = len(user_industries.intersection(career_industries))
                industry_score = industry_overlap / len(user_industries)
                score += industry_score * 0.1
            
            # Interest matching (5% weight)
            career_text = f"{career.title} {getattr(career, 'description', '')}".lower()
            interest_matches = sum(1 for interest in user_interests if interest in career_text)
            if user_interests:
                interest_score = interest_matches / len(user_interests)
                score += interest_score * 0.05
            
            career_scores.append((career, score))
        
        # Sort by enhanced score
        career_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Take top candidates with minimum score threshold
        min_score_threshold = 0.15  # Minimum relevance threshold
        filtered_careers = [
            career for career, score in career_scores 
            if score >= min_score_threshold
        ][:self.config.prefilter_limit]
        
        # If too few results, relax threshold
        if len(filtered_careers) < 10:
            filtered_careers = [career for career, score in career_scores[:self.config.prefilter_limit]]
        
        logger.info(f"Enhanced pre-filtering completed: {len(filtered_careers)} careers selected from {len(available_careers)}")
        
        return filtered_careers
    
    def _apply_enhanced_sorting(
        self, 
        recommendations: List[CareerRecommendation], 
        user_profile: UserProfile
    ) -> List[CareerRecommendation]:
        """
        Apply enhanced sorting that considers field transitions and appropriateness.
        
        Args:
            recommendations: List of recommendations to sort
            user_profile: User profile for context
            
        Returns:
            Sorted list of recommendations
        """
        from .enhanced_categorization import (
            determine_enhanced_user_career_field, 
            get_enhanced_career_field
        )
        
        user_field, _ = determine_enhanced_user_career_field(user_profile)
        user_seniority = self._get_user_seniority_level(user_profile)
        
        def sort_key(rec: dict):
            career_field, _ = get_enhanced_career_field(rec['career'])
            
            # Base score
            base_score = rec['score'].total_score
            
            # Field alignment bonus
            field_bonus = 0.0
            if user_field == career_field:
                field_bonus = 0.1
            elif career_field in ['executive_leadership'] and user_seniority in ['senior', 'executive']:
                field_bonus = 0.05
            
            # Confidence bonus
            confidence_bonus = rec['confidence'] * 0.05
            
            return base_score + field_bonus + confidence_bonus
        
        recommendations.sort(key=sort_key, reverse=True)
        return recommendations
    
    def _get_user_seniority_level(self, user_profile: UserProfile) -> str:
        """Extract user's seniority level from their profile."""
        from .enhanced_categorization import extract_seniority_level
        
        if hasattr(user_profile, 'professional_data') and user_profile.professional_data:
            for exp in user_profile.professional_data.experience:
                seniority = extract_seniority_level(exp.title)
                if seniority != 'mid':  # If we find a specific seniority, use it
                    return seniority
        
        # Fallback to experience years
        total_years = sum(exp.duration_years for exp in user_profile.professional_data.experience) if hasattr(user_profile, 'professional_data') and user_profile.professional_data else 0
        
        if total_years >= 15:
            return 'executive'
        elif total_years >= 8:
            return 'senior'
        elif total_years >= 3:
            return 'mid'
        else:
            return 'junior'
    
    def get_recommendations_by_category(
        self,
        user_profile: UserProfile,
        available_careers: List[Career],
        limit_per_category: int = 5,
        exploration_level: int = 3
    ) -> Dict[str, List[CareerRecommendation]]:
        """Get recommendations organized by category using enhanced logic."""
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
        """Generate detailed explanation with enhanced field analysis."""
        from .enhanced_categorization import get_enhanced_career_field, determine_enhanced_user_career_field
        
        # Score the individual career
        score = self.scoring_engine.score_career(user_profile, career, exploration_level)
        
        # Categorize it
        recommendations = self.categorization_engine.categorize_recommendations(
            user_profile, [career], [score]
        )
        
        if not recommendations:
            return {"error": "Could not generate explanation"}
        
        recommendation = recommendations[0]
        
        # Enhanced explanation with field analysis
        user_field, user_field_confidence = determine_enhanced_user_career_field(user_profile)
        career_field, career_field_confidence = get_enhanced_career_field(career)
        
        return {
            "career_title": career.title,
            "total_score": score.total_score,
            "category": recommendation.category.value,
            "confidence": recommendation.confidence,
            "reasons": recommendation.reasons,
            "field_analysis": {
                "user_field": user_field,
                "user_field_confidence": user_field_confidence,
                "career_field": career_field,
                "career_field_confidence": career_field_confidence,
                "field_transition": "same_field" if user_field == career_field else "field_change"
            },
            "score_breakdown": {
                "skill_match": score.skill_match_score,
                "interest_match": score.interest_match_score,
                "salary_compatibility": score.salary_compatibility_score,
                "experience_match": score.experience_match_score,
                "consistency_penalty": score.consistency_penalty
            },
            "detailed_breakdown": score.breakdown
        }
    def refine_recommendations(
        self,
        current_recommendations: List[CareerRecommendation],
        prompt: str,
        user_profile: UserProfile,
        exploration_level: int = 3
    ) -> List[CareerRecommendation]:
        """
        Refine recommendations based on user's textual prompt.
        
        Args:
            current_recommendations: The current list of recommendations
            prompt: The user's textual prompt for refinement
            user_profile: The user's profile for context
            exploration_level: User's exploration level (1-5)
            
        Returns:
            A new list of refined career recommendations
        """
        logger.info(f"Starting recommendation refinement with prompt: '{prompt}'")

        prompt_keywords = set(prompt.lower().split())
        
        refined_recommendations = []
        for rec in current_recommendations:
            career_text = f"{rec.career.title} {rec.career.description}".lower()
            
            # Simple keyword matching for boosting
            matches = sum(1 for keyword in prompt_keywords if keyword in career_text)
            
            # Boost score based on matches
            boost = matches * 0.1
            rec.score.total_score = min(1.0, rec.score.total_score + boost)
            
            refined_recommendations.append(rec)
            
        # Re-sort recommendations based on new scores
        refined_recommendations.sort(key=lambda x: x.score.total_score, reverse=True)
        
        logger.info(f"Generated {len(refined_recommendations)} refined recommendations")
        
        return refined_recommendations
    
    # Include all the helper methods from the original engine
    def _fallback_filtering(
        self, 
        user_profile: UserProfile, 
        available_careers: List[Career]
    ) -> List[Career]:
        """Fallback filtering when initial filtering returns no results."""
        relaxed_careers = self.filter_engine.apply_initial_filters(user_profile, available_careers)
        
        if relaxed_careers:
            return relaxed_careers
        
        return available_careers[:self.config.max_recommendations]
    
    def _ensure_minimum_recommendations(
        self,
        user_profile: UserProfile,
        available_careers: List[Career],
        current_recommendations: List[CareerRecommendation],
        exploration_level: int = 3
    ) -> List[CareerRecommendation]:
        """Ensure minimum number of recommendations."""
        if len(current_recommendations) >= self.config.min_recommendations:
            return current_recommendations
        
        recommended_ids = {rec.career.career_id for rec in current_recommendations}
        remaining_careers = [
            career for career in available_careers
            if career.career_id not in recommended_ids
        ]
        
        remaining_scores = self.scoring_engine.score_multiple_careers(
            user_profile, remaining_careers, exploration_level
        )
        
        additional_recommendations = self.categorization_engine.categorize_recommendations(
            user_profile, remaining_careers, remaining_scores
        )
        
        needed = self.config.min_recommendations - len(current_recommendations)
        additional_recommendations.sort(key=lambda x: x.score.total_score, reverse=True)
        
        return current_recommendations + additional_recommendations[:needed]
    
    def _preprocess_user_profile(self, user_profile: UserProfile) -> Dict:
        """Preprocess user profile for enhanced filtering."""
        logger.info("Starting enhanced user profile preprocessing")
        
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
        
        if hasattr(user_profile, 'resumeText') and user_profile.resumeText:
            resume_text = user_profile.resumeText.strip()
            if len(resume_text) > 500:
                summary["resume_summary"] = resume_text[:500] + "..."
            else:
                summary["resume_summary"] = resume_text
        else:
            summary["resume_summary"] = ""
        
        logger.info(f"Enhanced user profile preprocessed: {len(summary['key_skills'])} skills, "
                   f"{len(summary['primary_industries'])} industries")
        
        return summary
    
    def _validate_prompt_size(
        self,
        user_profile: UserProfile,
        careers: List[Career],
        max_size: int = MAX_PROMPT_SIZE
    ) -> tuple[List[Career], bool]:
        """Validate prompt size and truncate if necessary."""
        logger.info(f"Validating prompt size for {len(careers)} careers")
        
        try:
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
                        "description": career.description[:200],
                        "required_skills": [skill.name for skill in career.required_skills],
                        "salary_range": career.salary_range.dict(),
                        "career_field": career.career_field
                    }
                    for career in careers
                ]
            }
            
            estimated_size = len(json.dumps(prompt_data, default=str))
            logger.info(f"Estimated prompt size: {estimated_size} characters")
            
            if estimated_size <= max_size:
                return careers, False
            
            logger.warning(f"Prompt size ({estimated_size}) exceeds limit ({max_size}). Truncating careers list.")
            
            # Binary search for optimal career count
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
            fallback_limit = min(MAX_CAREERS_FOR_PROMPT, len(careers))
            logger.warning(f"Using fallback limit of {fallback_limit} careers due to validation error")
            return careers[:fallback_limit], len(careers) > fallback_limit