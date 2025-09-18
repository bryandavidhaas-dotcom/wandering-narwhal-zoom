"""
Filtering logic for the recommendation engine.

This module implements multi-stage filtering to narrow down career recommendations
based on user preferences, skills, and interests.
"""

from typing import List, Dict, Set, Optional
from datetime import datetime, timedelta
from .models import UserProfile, Career, Skill, SkillLevel, InterestLevel
from .config import FilteringConfig


class FilterEngine:
    """
    Engine for filtering careers based on user profile and preferences.
    
    Implements multi-stage filtering:
    1. Initial filtering (salary, location, basic requirements)
    2. Skill-based filtering (skill overlap and requirements)
    3. Interest-based filtering (alignment with user interests)
    """
    
    def __init__(self, config: FilteringConfig, skills_db: List[Skill]):
        """
        Initialize the filter engine.
        
        Args:
            config: Filtering configuration
            skills_db: Database of all available skills for related skill lookup
        """
        self.config = config
        self.skills_db = {skill.skill_id: skill for skill in skills_db}
        self.skill_name_to_id = {skill.name.lower(): skill.skill_id for skill in skills_db}
    
    def filter_careers(self, user_profile: UserProfile, careers: List[Career]) -> List[Career]:
        """
        Apply all filtering stages to get relevant careers for the user.
        
        Args:
            user_profile: User's profile with preferences and skills
            careers: List of all available careers
            
        Returns:
            List of filtered careers that match user criteria
        """
        # Stage 1: Initial filtering
        filtered_careers = self.apply_initial_filters(user_profile, careers)
        
        # Stage 2: Skill-based filtering
        filtered_careers = self.apply_skill_filters(user_profile, filtered_careers)
        
        # Stage 3: Interest-based filtering
        filtered_careers = self.apply_interest_filters(user_profile, filtered_careers)
        
        return filtered_careers
    
    def apply_initial_filters(self, user_profile: UserProfile, careers: List[Career]) -> List[Career]:
        """
        Apply initial filters based on salary expectations and basic preferences.
        
        Args:
            user_profile: User's profile with salary expectations
            careers: List of careers to filter
            
        Returns:
            List of careers that pass initial filtering
        """
        filtered_careers = []
        
        for career in careers:
            # Check salary compatibility
            if not self._is_salary_compatible(user_profile, career):
                continue
            
            # Add other initial filters here (location, work style, etc.)
            # For now, we'll focus on salary as the main initial filter
            
            filtered_careers.append(career)
        
        return filtered_careers
    
    def apply_skill_filters(self, user_profile: UserProfile, careers: List[Career]) -> List[Career]:
        """
        Apply skill-based filtering to ensure minimum skill overlap.
        
        Args:
            user_profile: User's profile with skills
            careers: List of careers to filter
            
        Returns:
            List of careers that meet skill requirements
        """
        filtered_careers = []
        user_skills = self._get_user_skill_set(user_profile)
        
        for career in careers:
            skill_overlap = self._calculate_skill_overlap(user_profile, career)
            
            # Check if skill overlap meets minimum threshold
            if skill_overlap >= self.config.min_skill_overlap:
                filtered_careers.append(career)
            # Also include careers where user has all mandatory skills
            elif self._has_mandatory_skills(user_profile, career):
                filtered_careers.append(career)
        
        return filtered_careers
    
    def apply_interest_filters(self, user_profile: UserProfile, careers: List[Career]) -> List[Career]:
        """
        Apply interest-based filtering to align with user preferences.
        
        Args:
            user_profile: User's profile with interests
            careers: List of careers to filter
            
        Returns:
            List of careers that align with user interests
        """
        # For now, we'll be permissive with interest filtering
        # In a more sophisticated implementation, we could filter out
        # careers that strongly conflict with user interests
        
        filtered_careers = []
        
        for career in careers:
            interest_alignment = self._calculate_interest_alignment(user_profile, career)
            
            # Keep careers with at least some interest alignment
            # or if the user hasn't specified strong negative interests
            if interest_alignment > 0.1 or not self._has_conflicting_interests(user_profile, career):
                filtered_careers.append(career)
        
        return filtered_careers
    
    def _is_salary_compatible(self, user_profile: UserProfile, career: Career) -> bool:
        """
        Check if career salary range is compatible with user expectations.
        
        Args:
            user_profile: User profile with salary expectations
            career: Career with salary range
            
        Returns:
            True if salary ranges are compatible within deviation threshold
        """
        if not user_profile.personal_info.salary_expectations:
            return True  # No salary expectations specified
        
        user_salary = user_profile.personal_info.salary_expectations
        career_salary = career.salary_range
        
        # Check currency compatibility
        if user_salary.currency != career_salary.currency:
            return True  # For now, assume compatible if different currencies
        
        # Calculate overlap considering deviation tolerance
        user_min = user_salary.min * (1 - self.config.max_salary_deviation)
        user_max = user_salary.max * (1 + self.config.max_salary_deviation)
        
        # Check if there's any overlap between ranges
        return not (career_salary.max < user_min or career_salary.min > user_max)
    
    def _get_user_skill_set(self, user_profile: UserProfile) -> Set[str]:
        """
        Get set of user skill names (normalized to lowercase).
        
        Args:
            user_profile: User profile with skills
            
        Returns:
            Set of skill names the user possesses
        """
        skill_set = set()
        
        # Add skills from user's skill list
        for skill in user_profile.skills:
            skill_set.add(skill.name.lower())
        
        # Add skills from professional data
        for skill_name in user_profile.professional_data.resume_skills:
            skill_set.add(skill_name.lower())
        
        for skill_name in user_profile.professional_data.linkedin_skills:
            skill_set.add(skill_name.lower())
        
        # Add related skills if configured
        if self.config.consider_related_skills:
            skill_set.update(self._get_related_skills(skill_set))
        
        return skill_set
    
    def _get_related_skills(self, user_skills: Set[str]) -> Set[str]:
        """
        Get related skills based on user's existing skills.
        
        Args:
            user_skills: Set of user's skill names
            
        Returns:
            Set of related skill names
        """
        related_skills = set()
        
        for skill_name in user_skills:
            skill_id = self.skill_name_to_id.get(skill_name)
            if skill_id and skill_id in self.skills_db:
                skill = self.skills_db[skill_id]
                for related_id in skill.related_skills:
                    if related_id in self.skills_db:
                        related_skill_name = self.skills_db[related_id].name.lower()
                        related_skills.add(related_skill_name)
        
        return related_skills
    
    def _calculate_skill_overlap(self, user_profile: UserProfile, career: Career) -> float:
        """
        Calculate the overlap between user skills and career requirements.
        
        Args:
            user_profile: User profile with skills
            career: Career with required skills
            
        Returns:
            Skill overlap ratio (0.0 to 1.0)
        """
        if not career.required_skills:
            return 1.0  # No requirements means perfect match
        
        user_skills = self._get_user_skill_set(user_profile)
        required_skills = {skill.name.lower() for skill in career.required_skills}
        
        if not required_skills:
            return 1.0
        
        overlap = len(user_skills.intersection(required_skills))
        return overlap / len(required_skills)
    
    def _has_mandatory_skills(self, user_profile: UserProfile, career: Career) -> bool:
        """
        Check if user has all mandatory skills for the career.
        
        Args:
            user_profile: User profile with skills
            career: Career with required skills
            
        Returns:
            True if user has all mandatory skills
        """
        user_skills = self._get_user_skill_set(user_profile)
        mandatory_skills = {
            skill.name.lower() for skill in career.required_skills 
            if skill.is_mandatory
        }
        
        return mandatory_skills.issubset(user_skills)
    
    def _calculate_interest_alignment(self, user_profile: UserProfile, career: Career) -> float:
        """
        Calculate alignment between user interests and career.
        
        Args:
            user_profile: User profile with interests
            career: Career to evaluate
            
        Returns:
            Interest alignment score (0.0 to 1.0)
        """
        if not user_profile.assessment_results.interests:
            return 0.5  # Neutral if no interests specified
        
        # Simple keyword matching between interests and career description/title
        career_text = (career.title + " " + career.description).lower()
        user_interests = user_profile.assessment_results.interests
        
        total_score = 0.0
        total_weight = 0.0
        
        for interest, level in user_interests.items():
            weight = self._interest_level_to_weight(level)
            total_weight += weight
            
            # Check if interest appears in career description
            if interest.lower() in career_text:
                total_score += weight
        
        if total_weight == 0:
            return 0.5
        
        return total_score / total_weight
    
    def _has_conflicting_interests(self, user_profile: UserProfile, career: Career) -> bool:
        """
        Check if career conflicts with user's strong negative interests.
        
        Args:
            user_profile: User profile with interests
            career: Career to evaluate
            
        Returns:
            True if there are strong conflicts
        """
        # For now, we'll assume no strong conflicts
        # This could be enhanced to check for interests marked as "very low"
        # that appear prominently in the career description
        
        user_interests = user_profile.assessment_results.interests
        career_text = (career.title + " " + career.description).lower()
        
        for interest, level in user_interests.items():
            if level == InterestLevel.LOW and interest.lower() in career_text:
                # Check if this is a core aspect of the career
                if interest.lower() in career.title.lower():
                    return True
        
        return False
    
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
    
    def get_filter_statistics(self, user_profile: UserProfile, original_careers: List[Career]) -> Dict[str, int]:
        """
        Get statistics about filtering results.
        
        Args:
            user_profile: User profile
            original_careers: Original list of careers before filtering
            
        Returns:
            Dictionary with filtering statistics
        """
        stats = {
            "original_count": len(original_careers),
            "after_initial_filters": 0,
            "after_skill_filters": 0,
            "after_interest_filters": 0
        }
        
        # Apply filters step by step and count results
        after_initial = self.apply_initial_filters(user_profile, original_careers)
        stats["after_initial_filters"] = len(after_initial)
        
        after_skill = self.apply_skill_filters(user_profile, after_initial)
        stats["after_skill_filters"] = len(after_skill)
        
        after_interest = self.apply_interest_filters(user_profile, after_skill)
        stats["after_interest_filters"] = len(after_interest)
        
        return stats