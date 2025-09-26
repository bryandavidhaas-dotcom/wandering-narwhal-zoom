"""
Enhanced filtering logic for the recommendation engine.

This module implements advanced filtering to ensure appropriate recommendations
for different user types (students, trades professionals, experienced professionals)
and prevents cross-industry/experience level mismatches.
"""

from typing import List, Dict, Set, Optional
from datetime import datetime, timedelta
from .models import UserProfile, Career, Skill, SkillLevel, InterestLevel, ExperienceLevel
from .config import FilteringConfig
from enum import Enum


class UserType(str, Enum):
    """User type classification for targeted filtering."""
    STUDENT = "student"
    ENTRY_LEVEL = "entry_level"
    TRADES_PROFESSIONAL = "trades_professional"
    PROFESSIONAL = "professional"
    SENIOR_PROFESSIONAL = "senior_professional"


class IndustryCategory(str, Enum):
    """Industry categories for career alignment."""
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    TRADES = "trades"
    BUSINESS = "business"
    EDUCATION = "education"
    CREATIVE = "creative"
    FINANCE = "finance"
    MANUFACTURING = "manufacturing"
    SERVICE = "service"


class EnhancedFilterEngine:
    """
    Enhanced filtering engine that prevents inappropriate cross-industry,
    cross-experience level, and cross-career path recommendations.
    """
    
    def __init__(self, config: FilteringConfig, skills_db: List[Skill]):
        """Initialize the enhanced filter engine."""
        self.config = config
        self.skills_db = {skill.skill_id: skill for skill in skills_db}
        self.skill_name_to_id = {skill.name.lower(): skill.skill_id for skill in skills_db}
        
        # Define industry mappings
        self.career_industry_mapping = self._build_career_industry_mapping()
        self.skill_industry_mapping = self._build_skill_industry_mapping()
    
    def filter_careers(self, user_profile: UserProfile, careers: List[Career]) -> List[Career]:
        """
        Apply enhanced filtering to ensure appropriate career recommendations.
        
        Args:
            user_profile: User's profile with preferences and skills
            careers: List of all available careers
            
        Returns:
            List of appropriately filtered careers
        """
        # Step 1: Classify user type
        user_type = self._classify_user_type(user_profile)
        user_experience_level = self._determine_user_experience_level(user_profile)
        user_industries = self._determine_user_industries(user_profile)
        
        # Step 2: Apply basic filters
        filtered_careers = self._apply_basic_filters(user_profile, careers)
        
        # Step 3: Apply experience level filtering
        filtered_careers = self._apply_experience_level_filtering(
            user_profile, filtered_careers, user_type, user_experience_level
        )
        
        # Step 4: Apply industry alignment filtering
        filtered_careers = self._apply_industry_alignment_filtering(
            user_profile, filtered_careers, user_industries
        )
        
        # Step 5: Apply career path coherence filtering
        filtered_careers = self._apply_career_path_coherence_filtering(
            user_profile, filtered_careers, user_type
        )
        
        # Step 6: Apply skill-based filtering
        filtered_careers = self._apply_skill_filters(user_profile, filtered_careers)
        
        return filtered_careers
    
    def _classify_user_type(self, user_profile: UserProfile) -> UserType:
        """Classify user type based on profile data."""
        total_experience = sum(exp.duration_years for exp in user_profile.professional_data.experience)
        education = user_profile.professional_data.education or ""
        
        # Check if student
        if ("student" in education.lower() or 
            "bachelor" in education.lower() and total_experience < 1 or
            user_profile.personal_info.age and user_profile.personal_info.age < 22):
            return UserType.STUDENT
        
        # Check if trades professional
        trades_keywords = ["trade", "apprentice", "technician", "mechanic", "electrician", 
                          "plumber", "carpenter", "welder", "hvac"]
        user_skills_text = " ".join([skill.name.lower() for skill in user_profile.skills])
        experience_text = " ".join([exp.title.lower() for exp in user_profile.professional_data.experience])
        
        if any(keyword in user_skills_text or keyword in experience_text for keyword in trades_keywords):
            return UserType.TRADES_PROFESSIONAL
        
        # Classify by experience level
        if total_experience < 2:
            return UserType.ENTRY_LEVEL
        elif total_experience >= 8:
            return UserType.SENIOR_PROFESSIONAL
        else:
            return UserType.PROFESSIONAL
    
    def _determine_user_experience_level(self, user_profile: UserProfile) -> ExperienceLevel:
        """Determine user's experience level."""
        total_experience = sum(exp.duration_years for exp in user_profile.professional_data.experience)
        
        if total_experience < 1:
            return ExperienceLevel.ENTRY
        elif total_experience < 3:
            return ExperienceLevel.JUNIOR
        elif total_experience < 7:
            return ExperienceLevel.MID
        elif total_experience < 12:
            return ExperienceLevel.SENIOR
        else:
            return ExperienceLevel.EXPERT
    
    def _determine_user_industries(self, user_profile: UserProfile) -> Set[IndustryCategory]:
        """Determine user's industry background and interests."""
        industries = set()
        
        # Analyze experience
        for exp in user_profile.professional_data.experience:
            industry = self._classify_experience_industry(exp.title, exp.description or "")
            if industry:
                industries.add(industry)
        
        # Analyze skills
        for skill in user_profile.skills:
            industry = self._classify_skill_industry(skill.name)
            if industry:
                industries.add(industry)
        
        # If no clear industry, allow broader matching
        if not industries:
            industries.add(IndustryCategory.BUSINESS)  # Default to business as most transferable
        
        return industries
    
    def _apply_experience_level_filtering(
        self, 
        user_profile: UserProfile, 
        careers: List[Career], 
        user_type: UserType,
        user_experience_level: ExperienceLevel
    ) -> List[Career]:
        """Filter careers based on appropriate experience level."""
        filtered_careers = []
        
        for career in careers:
            career_experience_requirement = self._determine_career_experience_requirement(career)
            
            # Define allowed experience level transitions
            if user_type == UserType.STUDENT:
                # Students should only see entry-level positions
                if career_experience_requirement in [ExperienceLevel.ENTRY, ExperienceLevel.JUNIOR]:
                    filtered_careers.append(career)
            
            elif user_type == UserType.ENTRY_LEVEL:
                # Entry-level professionals can see entry to junior positions
                if career_experience_requirement in [ExperienceLevel.ENTRY, ExperienceLevel.JUNIOR]:
                    filtered_careers.append(career)
            
            elif user_type == UserType.TRADES_PROFESSIONAL:
                # Trades professionals should see trades careers or transferable skills
                if (self._is_trades_career(career) or 
                    career_experience_requirement <= self._experience_level_to_enum(user_experience_level, 1)):
                    filtered_careers.append(career)
            
            elif user_type == UserType.PROFESSIONAL:
                # Professionals can see careers within 1-2 levels of their experience
                max_level = self._experience_level_to_enum(user_experience_level, 2)
                min_level = self._experience_level_to_enum(user_experience_level, -1)
                if min_level <= career_experience_requirement <= max_level:
                    filtered_careers.append(career)
            
            elif user_type == UserType.SENIOR_PROFESSIONAL:
                # Senior professionals should see mid to expert level positions
                if career_experience_requirement in [ExperienceLevel.MID, ExperienceLevel.SENIOR, ExperienceLevel.EXPERT]:
                    filtered_careers.append(career)
        
        return filtered_careers
    
    def _apply_industry_alignment_filtering(
        self, 
        user_profile: UserProfile, 
        careers: List[Career],
        user_industries: Set[IndustryCategory]
    ) -> List[Career]:
        """Filter careers to maintain industry alignment."""
        filtered_careers = []
        
        for career in careers:
            career_industry = self._classify_career_industry(career)
            
            # Allow career if:
            # 1. It's in user's current industry
            # 2. It's in a transferable industry
            # 3. It's a general business role
            if (career_industry in user_industries or
                self._is_transferable_industry_match(user_industries, career_industry) or
                career_industry == IndustryCategory.BUSINESS):
                filtered_careers.append(career)
        
        return filtered_careers
    
    def _apply_career_path_coherence_filtering(
        self, 
        user_profile: UserProfile, 
        careers: List[Career],
        user_type: UserType
    ) -> List[Career]:
        """Ensure career recommendations make logical sense for career progression."""
        filtered_careers = []
        
        for career in careers:
            if self._is_coherent_career_transition(user_profile, career, user_type):
                filtered_careers.append(career)
        
        return filtered_careers
    
    def _is_coherent_career_transition(
        self, 
        user_profile: UserProfile, 
        career: Career, 
        user_type: UserType
    ) -> bool:
        """Check if career transition makes logical sense."""
        
        # For students - any entry-level career is coherent
        if user_type == UserType.STUDENT:
            return True
        
        # For trades professionals - must be trades-related or have transferable skills
        if user_type == UserType.TRADES_PROFESSIONAL:
            if self._is_trades_career(career):
                return True
            # Check for transferable skills
            user_skills = {skill.name.lower() for skill in user_profile.skills}
            career_skills = {skill.name.lower() for skill in career.required_skills}
            overlap = len(user_skills.intersection(career_skills)) / max(len(career_skills), 1)
            return overlap >= 0.3  # At least 30% skill overlap
        
        # For professionals - check skill transferability and logical progression
        user_skills = {skill.name.lower() for skill in user_profile.skills}
        career_skills = {skill.name.lower() for skill in career.required_skills}
        
        if not career_skills:  # No specific requirements
            return True
        
        # Calculate skill overlap
        overlap = len(user_skills.intersection(career_skills)) / len(career_skills)
        
        # Require at least 20% skill overlap for coherent transition
        return overlap >= 0.2
    
    def _determine_career_experience_requirement(self, career: Career) -> ExperienceLevel:
        """Determine the experience level required for a career."""
        # Analyze career title and description for experience indicators
        title_lower = career.title.lower()
        desc_lower = career.description.lower()
        
        senior_keywords = ["senior", "lead", "principal", "director", "manager", "head"]
        mid_keywords = ["mid", "intermediate", "specialist", "analyst"]
        junior_keywords = ["junior", "associate", "assistant", "entry"]
        
        if any(keyword in title_lower for keyword in senior_keywords):
            return ExperienceLevel.SENIOR
        elif any(keyword in title_lower for keyword in mid_keywords):
            return ExperienceLevel.MID
        elif any(keyword in title_lower for keyword in junior_keywords):
            return ExperienceLevel.JUNIOR
        
        # Analyze required skills complexity
        if career.required_skills:
            expert_skills = sum(1 for skill in career.required_skills 
                              if skill.proficiency in [SkillLevel.EXPERT, SkillLevel.ADVANCED])
            if expert_skills >= 3:
                return ExperienceLevel.SENIOR
            elif expert_skills >= 1:
                return ExperienceLevel.MID
        
        return ExperienceLevel.JUNIOR  # Default to junior level
    
    def _classify_career_industry(self, career: Career) -> IndustryCategory:
        """Classify career into industry category."""
        title_lower = career.title.lower()
        desc_lower = career.description.lower()
        
        # Technology
        tech_keywords = ["software", "developer", "engineer", "programmer", "data", "ai", "tech"]
        if any(keyword in title_lower or keyword in desc_lower for keyword in tech_keywords):
            return IndustryCategory.TECHNOLOGY
        
        # Trades
        trades_keywords = ["electrician", "plumber", "carpenter", "mechanic", "technician", "hvac"]
        if any(keyword in title_lower or keyword in desc_lower for keyword in trades_keywords):
            return IndustryCategory.TRADES
        
        # Healthcare
        health_keywords = ["nurse", "doctor", "medical", "health", "clinical", "therapy"]
        if any(keyword in title_lower or keyword in desc_lower for keyword in health_keywords):
            return IndustryCategory.HEALTHCARE
        
        # Business (default for management, sales, etc.)
        return IndustryCategory.BUSINESS
    
    def _classify_skill_industry(self, skill_name: str) -> Optional[IndustryCategory]:
        """Classify skill into industry category."""
        skill_lower = skill_name.lower()
        
        # Technology skills
        tech_skills = ["python", "javascript", "java", "sql", "react", "aws", "docker", "git"]
        if any(tech_skill in skill_lower for tech_skill in tech_skills):
            return IndustryCategory.TECHNOLOGY
        
        # Trades skills
        trades_skills = ["welding", "electrical", "plumbing", "carpentry", "hvac", "mechanical"]
        if any(trade_skill in skill_lower for trade_skill in trades_skills):
            return IndustryCategory.TRADES
        
        return None
    
    def _classify_experience_industry(self, title: str, description: str) -> Optional[IndustryCategory]:
        """Classify work experience into industry category."""
        text = (title + " " + description).lower()
        
        if any(keyword in text for keyword in ["software", "tech", "developer", "engineer"]):
            return IndustryCategory.TECHNOLOGY
        elif any(keyword in text for keyword in ["trade", "construction", "maintenance"]):
            return IndustryCategory.TRADES
        elif any(keyword in text for keyword in ["health", "medical", "clinical"]):
            return IndustryCategory.HEALTHCARE
        
        return IndustryCategory.BUSINESS
    
    def _is_trades_career(self, career: Career) -> bool:
        """Check if career is trades-related."""
        return self._classify_career_industry(career) == IndustryCategory.TRADES
    
    def _is_transferable_industry_match(
        self, 
        user_industries: Set[IndustryCategory], 
        career_industry: IndustryCategory
    ) -> bool:
        """Check if industry transition is reasonable."""
        # Define transferable industry pairs
        transferable_pairs = {
            IndustryCategory.TECHNOLOGY: {IndustryCategory.BUSINESS, IndustryCategory.FINANCE},
            IndustryCategory.BUSINESS: {IndustryCategory.TECHNOLOGY, IndustryCategory.FINANCE},
            IndustryCategory.TRADES: {IndustryCategory.MANUFACTURING, IndustryCategory.SERVICE},
        }
        
        for user_industry in user_industries:
            if career_industry in transferable_pairs.get(user_industry, set()):
                return True
        
        return False
    
    def _experience_level_to_enum(self, level: ExperienceLevel, offset: int = 0) -> ExperienceLevel:
        """Convert experience level with offset."""
        levels = [ExperienceLevel.ENTRY, ExperienceLevel.JUNIOR, ExperienceLevel.MID, 
                 ExperienceLevel.SENIOR, ExperienceLevel.EXPERT]
        
        current_index = levels.index(level)
        new_index = max(0, min(len(levels) - 1, current_index + offset))
        return levels[new_index]
    
    def _apply_basic_filters(self, user_profile: UserProfile, careers: List[Career]) -> List[Career]:
        """Apply basic salary and preference filters."""
        filtered_careers = []
        
        for career in careers:
            # Salary compatibility
            if self._is_salary_compatible(user_profile, career):
                filtered_careers.append(career)
        
        return filtered_careers
    
    def _apply_skill_filters(self, user_profile: UserProfile, careers: List[Career]) -> List[Career]:
        """Apply skill-based filtering."""
        filtered_careers = []
        user_skills = self._get_user_skill_set(user_profile)
        
        for career in careers:
            skill_overlap = self._calculate_skill_overlap(user_profile, career)
            
            # More lenient skill filtering - focus on potential rather than perfect match
            if (skill_overlap >= 0.1 or  # At least 10% overlap
                self._has_some_mandatory_skills(user_profile, career) or
                not career.required_skills):  # No specific requirements
                filtered_careers.append(career)
        
        return filtered_careers
    
    def _is_salary_compatible(self, user_profile: UserProfile, career: Career) -> bool:
        """Check salary compatibility with more flexible ranges."""
        if not user_profile.personal_info.salary_expectations:
            return True
        
        user_salary = user_profile.personal_info.salary_expectations
        career_salary = career.salary_range
        
        if user_salary.currency != career_salary.currency:
            return True  # Assume compatible for different currencies
        
        # More flexible salary matching - allow 50% deviation
        user_min = user_salary.min * 0.5
        user_max = user_salary.max * 1.5
        
        return not (career_salary.max < user_min or career_salary.min > user_max)
    
    def _get_user_skill_set(self, user_profile: UserProfile) -> Set[str]:
        """Get user's skill set."""
        skill_set = set()
        
        for skill in user_profile.skills:
            skill_set.add(skill.name.lower())
        
        for skill_name in user_profile.professional_data.resume_skills:
            skill_set.add(skill_name.lower())
        
        for skill_name in user_profile.professional_data.linkedin_skills:
            skill_set.add(skill_name.lower())
        
        return skill_set
    
    def _calculate_skill_overlap(self, user_profile: UserProfile, career: Career) -> float:
        """Calculate skill overlap ratio."""
        if not career.required_skills:
            return 1.0
        
        user_skills = self._get_user_skill_set(user_profile)
        required_skills = {skill.name.lower() for skill in career.required_skills}
        
        if not required_skills:
            return 1.0
        
        overlap = len(user_skills.intersection(required_skills))
        return overlap / len(required_skills)
    
    def _has_some_mandatory_skills(self, user_profile: UserProfile, career: Career) -> bool:
        """Check if user has at least some mandatory skills."""
        user_skills = self._get_user_skill_set(user_profile)
        mandatory_skills = {
            skill.name.lower() for skill in career.required_skills 
            if skill.is_mandatory
        }
        
        if not mandatory_skills:
            return True
        
        # User needs at least 50% of mandatory skills
        overlap = len(user_skills.intersection(mandatory_skills))
        return overlap >= len(mandatory_skills) * 0.5
    
    def _build_career_industry_mapping(self) -> Dict[str, IndustryCategory]:
        """Build mapping of career IDs to industries."""
        # This would be populated from a database in production
        return {}
    
    def _build_skill_industry_mapping(self) -> Dict[str, IndustryCategory]:
        """Build mapping of skills to industries."""
        # This would be populated from a database in production
        return {}