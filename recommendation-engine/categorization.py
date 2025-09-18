"""
Categorization logic for the recommendation engine.

This module implements the logic to categorize scored career recommendations
into Safe Zone, Stretch Zone, and Adventure Zone based on configurable thresholds.
"""

from typing import List, Dict
from .models import (
    Career, RecommendationScore, CareerRecommendation, 
    RecommendationCategory, UserProfile
)
from .config import CategorizationThresholds


class CategorizationEngine:
    """
    Engine for categorizing career recommendations into zones.
    
    Categories:
    - Safe Zone: High-confidence matches with existing skills and experience
    - Stretch Zone: Good matches that require some skill development
    - Adventure Zone: Interesting matches that require significant upskilling
    """
    
    def __init__(self, thresholds: CategorizationThresholds):
        """
        Initialize the categorization engine.
        
        Args:
            thresholds: Thresholds for different recommendation categories
        """
        self.thresholds = thresholds
    
    def categorize_recommendations(
        self, 
        user_profile: UserProfile,
        careers: List[Career], 
        scores: List[RecommendationScore]
    ) -> List[CareerRecommendation]:
        """
        Categorize career recommendations based on scores and user profile.
        
        Args:
            user_profile: User's profile for context
            careers: List of careers being recommended
            scores: Corresponding recommendation scores
            
        Returns:
            List of CareerRecommendation objects with categories and reasons
        """
        career_dict = {career.career_id: career for career in careers}
        recommendations = []
        
        for score in scores:
            career = career_dict.get(score.career_id)
            if not career:
                continue
            
            category = self._determine_category(score, user_profile, career)
            reasons = self._generate_reasons(score, user_profile, career, category)
            confidence = self._calculate_confidence(score, category)
            
            recommendation = CareerRecommendation(
                career=career,
                score=score,
                category=category,
                reasons=reasons,
                confidence=confidence
            )
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _determine_category(
        self, 
        score: RecommendationScore, 
        user_profile: UserProfile, 
        career: Career
    ) -> RecommendationCategory:
        """
        Determine the appropriate category for a recommendation.
        
        Args:
            score: Recommendation score
            user_profile: User's profile
            career: Career being categorized
            
        Returns:
            RecommendationCategory enum value
        """
        total_score = score.total_score
        skill_score = score.skill_match_score
        
        # Primary categorization based on total score
        if total_score >= self.thresholds.safe_zone_min:
            # High score - but check if it's truly "safe" based on skills
            if skill_score >= 0.8:
                return RecommendationCategory.SAFE_ZONE
            else:
                # High overall score but lower skill match - might be stretch
                return RecommendationCategory.STRETCH_ZONE
                
        elif total_score >= self.thresholds.stretch_zone_min:
            # Medium score - check skill requirements vs user skills
            missing_mandatory = self._count_missing_mandatory_skills(user_profile, career)
            
            if missing_mandatory == 0:
                return RecommendationCategory.SAFE_ZONE
            elif missing_mandatory <= 2:
                return RecommendationCategory.STRETCH_ZONE
            else:
                return RecommendationCategory.ADVENTURE_ZONE
                
        elif total_score >= self.thresholds.adventure_zone_min:
            # Lower score - likely adventure zone
            return RecommendationCategory.ADVENTURE_ZONE
        
        else:
            # Very low score - still adventure but with low confidence
            return RecommendationCategory.ADVENTURE_ZONE
    
    def _generate_reasons(
        self, 
        score: RecommendationScore, 
        user_profile: UserProfile, 
        career: Career,
        category: RecommendationCategory
    ) -> List[str]:
        """
        Generate human-readable reasons for the recommendation.
        
        Args:
            score: Recommendation score with breakdown
            user_profile: User's profile
            career: Career being recommended
            category: Assigned category
            
        Returns:
            List of reason strings
        """
        reasons = []
        
        # Skill-based reasons
        if score.skill_match_score >= 0.8:
            matched_skills = score.breakdown.get("skill_details", {}).get("matched_skills", [])
            if matched_skills:
                skill_names = [skill["name"] for skill in matched_skills[:3]]  # Top 3
                reasons.append(f"Strong match for your skills: {', '.join(skill_names)}")
        
        elif score.skill_match_score >= 0.5:
            matched_skills = score.breakdown.get("skill_details", {}).get("matched_skills", [])
            missing_skills = score.breakdown.get("skill_details", {}).get("missing_mandatory", [])
            
            if matched_skills:
                skill_names = [skill["name"] for skill in matched_skills[:2]]
                reasons.append(f"Good foundation with skills: {', '.join(skill_names)}")
            
            if missing_skills and len(missing_skills) <= 3:
                reasons.append(f"Would benefit from developing: {', '.join(missing_skills[:3])}")
        
        else:
            missing_skills = score.breakdown.get("skill_details", {}).get("missing_mandatory", [])
            if missing_skills:
                reasons.append(f"Opportunity to learn new skills: {', '.join(missing_skills[:3])}")
        
        # Interest-based reasons
        if score.interest_match_score >= 0.7:
            matched_interests = score.breakdown.get("interest_details", {}).get("matched_interests", [])
            if matched_interests:
                interest_names = [item["interest"] for item in matched_interests[:2]]
                reasons.append(f"Aligns with your interests in {', '.join(interest_names)}")
        
        # Salary-based reasons
        salary_details = score.breakdown.get("salary_details", {})
        compatibility = salary_details.get("compatibility", "unknown")
        
        if compatibility == "compatible":
            reasons.append("Salary range matches your expectations")
        elif compatibility == "higher_than_expected":
            reasons.append("Offers higher compensation than expected")
        elif compatibility == "too_low":
            reasons.append("Salary may be below your expectations")
        
        # Experience-based reasons
        experience_details = score.breakdown.get("experience_details", {})
        user_level = experience_details.get("experience_level", "unknown")
        
        if user_level in ["mid", "senior", "expert"]:
            reasons.append("Good match for your experience level")
        elif user_level in ["entry", "junior"]:
            if category == RecommendationCategory.STRETCH_ZONE:
                reasons.append("Great opportunity for career growth")
            elif category == RecommendationCategory.ADVENTURE_ZONE:
                reasons.append("Ambitious career move with growth potential")
        
        # Category-specific reasons
        if category == RecommendationCategory.SAFE_ZONE:
            reasons.append("Low risk transition with your current skill set")
        elif category == RecommendationCategory.STRETCH_ZONE:
            reasons.append("Achievable with some additional skill development")
        elif category == RecommendationCategory.ADVENTURE_ZONE:
            reasons.append("Exciting opportunity to explore a new career direction")
        
        # Market demand reasons
        if hasattr(career, 'demand'):
            if career.demand.value == "high":
                reasons.append("High market demand for this role")
            elif career.demand.value == "very_high":
                reasons.append("Excellent job market with high demand")
        
        return reasons[:5]  # Limit to top 5 reasons
    
    def _calculate_confidence(
        self, 
        score: RecommendationScore, 
        category: RecommendationCategory
    ) -> float:
        """
        Calculate confidence level for the recommendation.
        
        Args:
            score: Recommendation score
            category: Assigned category
            
        Returns:
            Confidence level (0.0 to 1.0)
        """
        base_confidence = score.total_score
        
        # Adjust confidence based on category
        if category == RecommendationCategory.SAFE_ZONE:
            # High confidence for safe zone recommendations
            return min(1.0, base_confidence + 0.1)
        
        elif category == RecommendationCategory.STRETCH_ZONE:
            # Moderate confidence adjustment
            return base_confidence
        
        elif category == RecommendationCategory.ADVENTURE_ZONE:
            # Lower confidence for adventure zone
            return max(0.3, base_confidence - 0.1)
        
        return base_confidence
    
    def _count_missing_mandatory_skills(self, user_profile: UserProfile, career: Career) -> int:
        """
        Count how many mandatory skills the user is missing.
        
        Args:
            user_profile: User's profile with skills
            career: Career with requirements
            
        Returns:
            Number of missing mandatory skills
        """
        user_skills = {skill.name.lower() for skill in user_profile.skills}
        mandatory_skills = {
            skill.name.lower() for skill in career.required_skills 
            if skill.is_mandatory
        }
        
        missing_skills = mandatory_skills - user_skills
        return len(missing_skills)
    
    def get_category_distribution(self, recommendations: List[CareerRecommendation]) -> Dict[str, int]:
        """
        Get distribution of recommendations across categories.
        
        Args:
            recommendations: List of categorized recommendations
            
        Returns:
            Dictionary with category counts
        """
        distribution = {
            "safe_zone": 0,
            "stretch_zone": 0,
            "adventure_zone": 0
        }
        
        for rec in recommendations:
            if rec.category == RecommendationCategory.SAFE_ZONE:
                distribution["safe_zone"] += 1
            elif rec.category == RecommendationCategory.STRETCH_ZONE:
                distribution["stretch_zone"] += 1
            elif rec.category == RecommendationCategory.ADVENTURE_ZONE:
                distribution["adventure_zone"] += 1
        
        return distribution
    
    def filter_by_category(
        self, 
        recommendations: List[CareerRecommendation], 
        category: RecommendationCategory
    ) -> List[CareerRecommendation]:
        """
        Filter recommendations by category.
        
        Args:
            recommendations: List of all recommendations
            category: Category to filter by
            
        Returns:
            List of recommendations in the specified category
        """
        return [rec for rec in recommendations if rec.category == category]
    
    def get_top_recommendations_per_category(
        self, 
        recommendations: List[CareerRecommendation], 
        limit_per_category: int = 3
    ) -> Dict[str, List[CareerRecommendation]]:
        """
        Get top recommendations for each category.
        
        Args:
            recommendations: List of all recommendations
            limit_per_category: Maximum recommendations per category
            
        Returns:
            Dictionary with top recommendations per category
        """
        categorized = {
            "safe_zone": [],
            "stretch_zone": [],
            "adventure_zone": []
        }
        
        for rec in recommendations:
            if rec.category == RecommendationCategory.SAFE_ZONE:
                categorized["safe_zone"].append(rec)
            elif rec.category == RecommendationCategory.STRETCH_ZONE:
                categorized["stretch_zone"].append(rec)
            elif rec.category == RecommendationCategory.ADVENTURE_ZONE:
                categorized["adventure_zone"].append(rec)
        
        # Sort each category by total score and limit
        for category in categorized:
            categorized[category].sort(key=lambda x: x.score.total_score, reverse=True)
            categorized[category] = categorized[category][:limit_per_category]
        
        return categorized