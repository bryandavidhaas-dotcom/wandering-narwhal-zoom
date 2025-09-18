"""
Main recommendation engine that orchestrates the entire recommendation process.

This module provides the primary RecommendationEngine class that coordinates
filtering, scoring, and categorization to generate career recommendations.
"""

from typing import List, Dict, Optional
from .models import UserProfile, Career, Skill, CareerRecommendation
from .config import RecommendationConfig, DEFAULT_CONFIG
from .filters import FilterEngine
from .scoring import ScoringEngine
from .categorization import CategorizationEngine


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
            self.config.scoring_weights
        )
        self.categorization_engine = CategorizationEngine(
            self.config.categorization_thresholds
        )
    
    def get_recommendations(
        self, 
        user_profile: UserProfile, 
        available_careers: List[Career],
        limit: Optional[int] = None
    ) -> List[CareerRecommendation]:
        """
        Generate career recommendations for a user.
        
        Args:
            user_profile: User's profile with skills, interests, and preferences
            available_careers: List of all available careers to consider
            limit: Maximum number of recommendations to return
            
        Returns:
            List of CareerRecommendation objects sorted by score
        """
        # Step 1: Filter careers based on user preferences and requirements
        filtered_careers = self.filter_engine.filter_careers(user_profile, available_careers)
        
        if not filtered_careers:
            # If no careers pass filtering, relax constraints and try again
            filtered_careers = self._fallback_filtering(user_profile, available_careers)
        
        # Step 2: Score the filtered careers
        scores = self.scoring_engine.score_multiple_careers(user_profile, filtered_careers)
        
        # Step 3: Categorize recommendations
        recommendations = self.categorization_engine.categorize_recommendations(
            user_profile, filtered_careers, scores
        )
        
        # Step 4: Apply final limits and sorting
        recommendations.sort(key=lambda x: x.score.total_score, reverse=True)
        
        if limit:
            recommendations = recommendations[:limit]
        elif len(recommendations) > self.config.max_recommendations:
            recommendations = recommendations[:self.config.max_recommendations]
        
        # Ensure minimum recommendations if possible
        if len(recommendations) < self.config.min_recommendations and len(available_careers) >= self.config.min_recommendations:
            recommendations = self._ensure_minimum_recommendations(
                user_profile, available_careers, recommendations
            )
        
        return recommendations
    
    def get_recommendations_by_category(
        self, 
        user_profile: UserProfile, 
        available_careers: List[Career],
        limit_per_category: int = 5
    ) -> Dict[str, List[CareerRecommendation]]:
        """
        Get recommendations organized by category.
        
        Args:
            user_profile: User's profile
            available_careers: List of available careers
            limit_per_category: Maximum recommendations per category
            
        Returns:
            Dictionary with recommendations organized by category
        """
        all_recommendations = self.get_recommendations(user_profile, available_careers)
        
        return self.categorization_engine.get_top_recommendations_per_category(
            all_recommendations, limit_per_category
        )
    
    def explain_recommendation(
        self, 
        user_profile: UserProfile, 
        career: Career
    ) -> Dict[str, any]:
        """
        Generate detailed explanation for why a career was recommended.
        
        Args:
            user_profile: User's profile
            career: Career to explain
            
        Returns:
            Dictionary with detailed explanation
        """
        # Score the individual career
        score = self.scoring_engine.score_career(user_profile, career)
        
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
                "experience_match": score.experience_match_score
            },
            "detailed_breakdown": score.breakdown
        }
    
    def get_recommendation_statistics(
        self, 
        user_profile: UserProfile, 
        available_careers: List[Career]
    ) -> Dict[str, any]:
        """
        Get statistics about the recommendation process.
        
        Args:
            user_profile: User's profile
            available_careers: List of available careers
            
        Returns:
            Dictionary with recommendation statistics
        """
        # Get filtering statistics
        filter_stats = self.filter_engine.get_filter_statistics(user_profile, available_careers)
        
        # Get recommendations
        recommendations = self.get_recommendations(user_profile, available_careers)
        
        # Get category distribution
        category_distribution = self.categorization_engine.get_category_distribution(recommendations)
        
        # Calculate score statistics
        if recommendations:
            scores = [rec.score.total_score for rec in recommendations]
            score_stats = {
                "average_score": sum(scores) / len(scores),
                "highest_score": max(scores),
                "lowest_score": min(scores),
                "score_range": max(scores) - min(scores)
            }
        else:
            score_stats = {
                "average_score": 0.0,
                "highest_score": 0.0,
                "lowest_score": 0.0,
                "score_range": 0.0
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
        current_recommendations: List[CareerRecommendation]
    ) -> List[CareerRecommendation]:
        """
        Ensure minimum number of recommendations by adding lower-scored options.
        
        Args:
            user_profile: User's profile
            available_careers: All available careers
            current_recommendations: Current recommendations
            
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
            user_profile, remaining_careers
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
            self.config.scoring_weights
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