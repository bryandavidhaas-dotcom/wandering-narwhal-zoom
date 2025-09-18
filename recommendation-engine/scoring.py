"""
Scoring algorithms for the recommendation engine.

This module implements weighted scoring algorithms to rank career recommendations
based on skill matching, interest alignment, salary compatibility, and experience.
"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from .models import (
    UserProfile, Career, RecommendationScore, SkillLevel, InterestLevel,
    UserSkill, RequiredSkill
)
from .config import ScoringConfig, ScoringWeights


class ScoringEngine:
    """
    Engine for scoring and ranking career recommendations.
    
    Implements weighted scoring based on:
    - Skill matching and proficiency levels
    - Interest alignment
    - Salary compatibility
    - Experience level matching
    """
    
    def __init__(self, scoring_config: ScoringConfig, scoring_weights: ScoringWeights):
        """
        Initialize the scoring engine.
        
        Args:
            scoring_config: Configuration for scoring algorithms
            scoring_weights: Weights for different scoring components
        """
        self.config = scoring_config
        self.weights = scoring_weights
        self.skill_level_order = [SkillLevel.BEGINNER, SkillLevel.INTERMEDIATE, SkillLevel.ADVANCED, SkillLevel.EXPERT]
    
    def score_career(self, user_profile: UserProfile, career: Career) -> RecommendationScore:
        """
        Calculate comprehensive score for a career recommendation.
        
        Args:
            user_profile: User's profile with skills and preferences
            career: Career to score
            
        Returns:
            RecommendationScore with detailed scoring breakdown
        """
        # Calculate individual component scores
        skill_score = self._calculate_skill_match_score(user_profile, career)
        interest_score = self._calculate_interest_match_score(user_profile, career)
        salary_score = self._calculate_salary_compatibility_score(user_profile, career)
        experience_score = self._calculate_experience_match_score(user_profile, career)
        
        # Calculate weighted total score
        total_score = (
            skill_score * self.weights.skill_match +
            interest_score * self.weights.interest_match +
            salary_score * self.weights.salary_compatibility +
            experience_score * self.weights.experience_match
        )
        
        # Create detailed breakdown
        breakdown = {
            "skill_details": self._get_skill_score_details(user_profile, career),
            "interest_details": self._get_interest_score_details(user_profile, career),
            "salary_details": self._get_salary_score_details(user_profile, career),
            "experience_details": self._get_experience_score_details(user_profile, career)
        }
        
        return RecommendationScore(
            career_id=career.career_id,
            total_score=min(1.0, max(0.0, total_score)),  # Clamp to [0, 1]
            skill_match_score=skill_score,
            interest_match_score=interest_score,
            salary_compatibility_score=salary_score,
            experience_match_score=experience_score,
            breakdown=breakdown
        )
    
    def score_multiple_careers(self, user_profile: UserProfile, careers: List[Career]) -> List[RecommendationScore]:
        """
        Score multiple careers and return sorted by total score.
        
        Args:
            user_profile: User's profile
            careers: List of careers to score
            
        Returns:
            List of RecommendationScore objects sorted by total score (descending)
        """
        scores = [self.score_career(user_profile, career) for career in careers]
        return sorted(scores, key=lambda x: x.total_score, reverse=True)
    
    def _calculate_skill_match_score(self, user_profile: UserProfile, career: Career) -> float:
        """
        Calculate skill matching score based on user skills vs career requirements.
        
        Args:
            user_profile: User profile with skills
            career: Career with required skills
            
        Returns:
            Skill match score (0.0 to 1.0)
        """
        if not career.required_skills:
            return 1.0  # Perfect score if no requirements
        
        user_skills_dict = {skill.name.lower(): skill for skill in user_profile.skills}
        total_weighted_score = 0.0
        total_weight = 0.0
        mandatory_penalty = 0.0
        
        for required_skill in career.required_skills:
            skill_name = required_skill.name.lower()
            weight = required_skill.weight
            total_weight += weight
            
            if skill_name in user_skills_dict:
                user_skill = user_skills_dict[skill_name]
                
                # Calculate proficiency match score
                proficiency_score = self._calculate_proficiency_match(
                    user_skill.level, required_skill.proficiency
                )
                
                # Apply bonuses
                bonus = 0.0
                if user_skill.is_certified:
                    bonus += self.config.certification_bonus
                
                if self._is_recent_experience(user_skill.last_used):
                    bonus += self.config.recent_experience_bonus
                
                skill_score = min(1.0, proficiency_score + bonus)
                total_weighted_score += skill_score * weight
                
            else:
                # Missing skill
                if required_skill.is_mandatory:
                    mandatory_penalty += self.config.mandatory_skill_penalty * weight
                # Non-mandatory missing skills get 0 score but no penalty
        
        if total_weight == 0:
            return 1.0
        
        base_score = total_weighted_score / total_weight
        final_score = max(0.0, base_score - mandatory_penalty)
        
        return min(1.0, final_score)
    
    def _calculate_interest_match_score(self, user_profile: UserProfile, career: Career) -> float:
        """
        Calculate interest alignment score.
        
        Args:
            user_profile: User profile with interests
            career: Career to evaluate
            
        Returns:
            Interest match score (0.0 to 1.0)
        """
        if not user_profile.assessment_results.interests:
            return 0.5  # Neutral score if no interests specified
        
        career_text = (career.title + " " + career.description).lower()
        user_interests = user_profile.assessment_results.interests
        
        total_score = 0.0
        total_weight = 0.0
        
        for interest, level in user_interests.items():
            weight = self._interest_level_to_weight(level)
            total_weight += weight
            
            # Simple keyword matching - could be enhanced with NLP
            if interest.lower() in career_text:
                total_score += weight
            
            # Check user's additional interests
            for user_interest in user_profile.user_interests:
                if user_interest.lower() in career_text:
                    total_score += 0.5  # Moderate bonus for additional interests
        
        if total_weight == 0:
            return 0.5
        
        # Normalize and add bonus for additional interest matches
        base_score = total_score / total_weight
        return min(1.0, base_score)
    
    def _calculate_salary_compatibility_score(self, user_profile: UserProfile, career: Career) -> float:
        """
        Calculate salary compatibility score.
        
        Args:
            user_profile: User profile with salary expectations
            career: Career with salary range
            
        Returns:
            Salary compatibility score (0.0 to 1.0)
        """
        if not user_profile.personal_info.salary_expectations:
            return 1.0  # Perfect score if no expectations
        
        user_salary = user_profile.personal_info.salary_expectations
        career_salary = career.salary_range
        
        # Handle different currencies (simplified)
        if user_salary.currency != career_salary.currency:
            return 0.8  # Slight penalty for currency mismatch
        
        # Calculate overlap between salary ranges
        overlap_start = max(user_salary.min, career_salary.min)
        overlap_end = min(user_salary.max, career_salary.max)
        
        if overlap_end < overlap_start:
            # No overlap - calculate distance penalty
            if career_salary.max < user_salary.min:
                # Career pays too little
                gap = user_salary.min - career_salary.max
                penalty = gap / user_salary.min
                return max(0.0, 1.0 - penalty)
            else:
                # Career pays more than expected (less penalty)
                gap = career_salary.min - user_salary.max
                penalty = gap / (user_salary.max * 2)  # Less penalty for higher pay
                return max(0.3, 1.0 - penalty)
        else:
            # There is overlap - calculate overlap ratio
            overlap_size = overlap_end - overlap_start
            user_range_size = user_salary.max - user_salary.min
            career_range_size = career_salary.max - career_salary.min
            
            # Score based on overlap relative to both ranges
            user_overlap_ratio = overlap_size / user_range_size if user_range_size > 0 else 1.0
            career_overlap_ratio = overlap_size / career_range_size if career_range_size > 0 else 1.0
            
            return (user_overlap_ratio + career_overlap_ratio) / 2
    
    def _calculate_experience_match_score(self, user_profile: UserProfile, career: Career) -> float:
        """
        Calculate experience level matching score.
        
        Args:
            user_profile: User profile with experience
            career: Career to evaluate
            
        Returns:
            Experience match score (0.0 to 1.0)
        """
        # Calculate total years of experience
        total_experience = sum(exp.duration_years for exp in user_profile.professional_data.experience)
        
        # Simple experience level mapping
        if total_experience < 1:
            user_level = "entry"
        elif total_experience < 3:
            user_level = "junior"
        elif total_experience < 7:
            user_level = "mid"
        elif total_experience < 12:
            user_level = "senior"
        else:
            user_level = "expert"
        
        # For now, assume all careers are suitable for mid-level
        # In a real implementation, careers would have experience requirements
        career_level = "mid"  # This would come from career data
        
        # Calculate experience match
        level_order = ["entry", "junior", "mid", "senior", "expert"]
        user_idx = level_order.index(user_level)
        career_idx = level_order.index(career_level)
        
        distance = abs(user_idx - career_idx)
        
        if distance == 0:
            return 1.0
        elif distance == 1:
            return 0.8
        elif distance == 2:
            return 0.6
        else:
            return 0.4
    
    def _calculate_proficiency_match(self, user_level: SkillLevel, required_level: SkillLevel) -> float:
        """
        Calculate how well user's skill level matches required level.
        
        Args:
            user_level: User's proficiency level
            required_level: Required proficiency level
            
        Returns:
            Proficiency match score (0.0 to 1.0)
        """
        user_idx = self.skill_level_order.index(user_level)
        required_idx = self.skill_level_order.index(required_level)
        
        if user_idx >= required_idx:
            # User meets or exceeds requirement
            return 1.0
        else:
            # User is below requirement
            gap = required_idx - user_idx
            return max(0.0, 1.0 - (gap * 0.25))  # 25% penalty per level gap
    
    def _is_recent_experience(self, last_used: datetime) -> bool:
        """
        Check if skill was used recently.
        
        Args:
            last_used: When the skill was last used
            
        Returns:
            True if skill was used within the last 6 months
        """
        if not last_used:
            return False
        
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        return last_used >= six_months_ago
    
    def _interest_level_to_weight(self, level: InterestLevel) -> float:
        """
        Convert interest level to numerical weight.
        
        Args:
            level: Interest level enum
            
        Returns:
            Numerical weight for the interest level
        """
        weights = {
            InterestLevel.LOW: 0.25,
            InterestLevel.MEDIUM: 0.5,
            InterestLevel.HIGH: 0.75,
            InterestLevel.VERY_HIGH: 1.0
        }
        return weights.get(level, 0.5)
    
    def _get_skill_score_details(self, user_profile: UserProfile, career: Career) -> Dict:
        """Get detailed breakdown of skill scoring."""
        details = {
            "matched_skills": [],
            "missing_mandatory": [],
            "missing_preferred": []
        }
        
        user_skills_dict = {skill.name.lower(): skill for skill in user_profile.skills}
        
        for required_skill in career.required_skills:
            skill_name = required_skill.name.lower()
            
            if skill_name in user_skills_dict:
                user_skill = user_skills_dict[skill_name]
                details["matched_skills"].append({
                    "name": required_skill.name,
                    "user_level": user_skill.level.value,
                    "required_level": required_skill.proficiency.value,
                    "is_certified": user_skill.is_certified
                })
            else:
                if required_skill.is_mandatory:
                    details["missing_mandatory"].append(required_skill.name)
                else:
                    details["missing_preferred"].append(required_skill.name)
        
        return details
    
    def _get_interest_score_details(self, user_profile: UserProfile, career: Career) -> Dict:
        """Get detailed breakdown of interest scoring."""
        career_text = (career.title + " " + career.description).lower()
        
        details = {
            "matched_interests": [],
            "user_interests": list(user_profile.assessment_results.interests.keys()),
            "additional_interests": user_profile.user_interests
        }
        
        for interest, level in user_profile.assessment_results.interests.items():
            if interest.lower() in career_text:
                details["matched_interests"].append({
                    "interest": interest,
                    "level": level.value
                })
        
        return details
    
    def _get_salary_score_details(self, user_profile: UserProfile, career: Career) -> Dict:
        """Get detailed breakdown of salary scoring."""
        details = {
            "user_expectations": None,
            "career_range": {
                "min": career.salary_range.min,
                "max": career.salary_range.max,
                "currency": career.salary_range.currency
            },
            "compatibility": "unknown"
        }
        
        if user_profile.personal_info.salary_expectations:
            user_salary = user_profile.personal_info.salary_expectations
            details["user_expectations"] = {
                "min": user_salary.min,
                "max": user_salary.max,
                "currency": user_salary.currency
            }
            
            # Determine compatibility
            if user_salary.currency != career.salary_range.currency:
                details["compatibility"] = "different_currency"
            elif career.salary_range.max < user_salary.min:
                details["compatibility"] = "too_low"
            elif career.salary_range.min > user_salary.max:
                details["compatibility"] = "higher_than_expected"
            else:
                details["compatibility"] = "compatible"
        
        return details
    
    def _get_experience_score_details(self, user_profile: UserProfile, career: Career) -> Dict:
        """Get detailed breakdown of experience scoring."""
        total_experience = sum(exp.duration_years for exp in user_profile.professional_data.experience)
        
        return {
            "total_years": total_experience,
            "experience_level": self._get_experience_level(total_experience),
            "relevant_experience": [
                {
                    "title": exp.title,
                    "duration": exp.duration_years,
                    "skills": exp.skills_used
                }
                for exp in user_profile.professional_data.experience
            ]
        }
    
    def _get_experience_level(self, years: float) -> str:
        """Convert years of experience to level string."""
        if years < 1:
            return "entry"
        elif years < 3:
            return "junior"
        elif years < 7:
            return "mid"
        elif years < 12:
            return "senior"
        else:
            return "expert"