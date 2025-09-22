"""
Unified API for the recommendation engine.

This module provides a single, unified API that integrates the enhanced categorization
system, career database, and all recommendation logic. This replaces the distributed
logic between frontend and backend.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
import logging
from datetime import datetime

from .enhanced_engine import EnhancedRecommendationEngine
from .career_database import CareerDatabase, CareerData, CareerField, ExperienceLevel
from .enhanced_categorization import get_enhanced_career_field, determine_enhanced_user_career_field
from .models import UserProfile, CareerRecommendation
from .config import DEFAULT_CONFIG

# Set up logging
logger = logging.getLogger(__name__)


@dataclass
class APIUserProfile:
    """
    Simplified user profile for API requests.
    
    This provides a clean interface for the frontend to send user data
    without needing to know the internal UserProfile structure.
    """
    # Basic Information
    user_id: str
    current_role: str = ""
    experience_years: float = 0.0
    education_level: str = "bachelors"
    location: str = ""
    
    # Skills
    technical_skills: List[str] = None
    soft_skills: List[str] = None
    certifications: List[str] = None
    
    # Work Preferences (1-5 scale)
    working_with_data: int = 3
    working_with_people: int = 3
    creative_tasks: int = 3
    problem_solving: int = 3
    leadership: int = 3
    physical_hands_on_work: int = 3
    mechanical_aptitude: int = 3
    outdoor_work: int = 3
    
    # Interests and Industries
    interests: List[str] = None
    industries: List[str] = None
    
    # Career Goals and Preferences
    career_goals: str = ""
    salary_expectations: Dict[str, int] = None  # {"min": 70000, "max": 120000, "currency": "USD"}
    work_life_balance_importance: int = 3
    remote_work_preference: str = "flexible"  # "required", "preferred", "flexible", "no"
    
    # Additional Context
    resume_text: str = ""
    linkedin_profile: str = ""
    
    def __post_init__(self):
        """Initialize default values for mutable fields."""
        if self.technical_skills is None:
            self.technical_skills = []
        if self.soft_skills is None:
            self.soft_skills = []
        if self.certifications is None:
            self.certifications = []
        if self.interests is None:
            self.interests = []
        if self.industries is None:
            self.industries = []
        if self.salary_expectations is None:
            self.salary_expectations = {"min": 50000, "max": 100000, "currency": "USD"}


@dataclass
class APICareerRecommendation:
    """
    API response format for career recommendations.
    
    This provides a clean, consistent format for the frontend to consume.
    """
    # Career Information
    career_id: str
    title: str
    description: str
    career_field: str
    experience_level: str
    
    # Salary Information
    salary_min: int
    salary_max: int
    salary_currency: str
    
    # Recommendation Metadata
    relevance_score: float  # 0.0 to 1.0
    confidence_level: float  # 0.0 to 1.0
    category: str  # "safe_zone", "stretch_zone", "adventure_zone"
    
    # Explanation
    match_reasons: List[str]
    skill_analysis: Dict[str, Any]
    field_analysis: Dict[str, Any]
    
    # Career Details
    required_skills: List[str]
    learning_path: str
    companies: List[str]
    work_environment: List[str]
    remote_options: str
    
    # Market Information
    demand_level: str
    growth_outlook: str


@dataclass
class APIRecommendationRequest:
    """Request format for getting recommendations."""
    user_profile: APIUserProfile
    exploration_level: int = 1  # 1=Safe, 2=Stretch, 3=Adventure
    limit: Optional[int] = 10
    career_fields: Optional[List[str]] = None
    experience_levels: Optional[List[str]] = None
    salary_range: Optional[Dict[str, int]] = None


@dataclass
class APIRecommendationResponse:
    """Response format for recommendation requests."""
    recommendations: List[APICareerRecommendation]
    user_analysis: Dict[str, Any]
    request_metadata: Dict[str, Any]
    total_careers_considered: int
    processing_time_ms: int


class UnifiedRecommendationAPI:
    """
    Unified API for career recommendations.
    
    This class provides a single, clean interface for all recommendation
    functionality, integrating the enhanced categorization system and
    career database.
    """
    
    def __init__(
        self, 
        career_db_path: str = "careers.db",
        use_enhanced_categorization: bool = True
    ):
        """
        Initialize the unified API.
        
        Args:
            career_db_path: Path to the career database
            use_enhanced_categorization: Whether to use enhanced categorization
        """
        self.career_db = CareerDatabase(career_db_path)
        self.recommendation_engine = EnhancedRecommendationEngine(
            config=DEFAULT_CONFIG,
            use_enhanced_categorization=use_enhanced_categorization
        )
        
        logger.info(f"Unified API initialized with database: {career_db_path}")
    
    def get_recommendations(self, request: APIRecommendationRequest) -> APIRecommendationResponse:
        """
        Get career recommendations for a user.
        
        Args:
            request: Recommendation request with user profile and preferences
            
        Returns:
            API response with recommendations and metadata
        """
        start_time = datetime.now()
        
        try:
            # Convert API user profile to internal format
            internal_profile = self._convert_api_profile_to_internal(request.user_profile)
            
            # Get careers from database with filters
            available_careers = self._get_filtered_careers(request)
            
            logger.info(f"Processing recommendations for user {request.user_profile.user_id} "
                       f"with {len(available_careers)} available careers")
            
            # Generate recommendations using enhanced engine
            recommendations = self.recommendation_engine.get_recommendations(
                user_profile=internal_profile,
                available_careers=available_careers,
                limit=request.limit,
                exploration_level=request.exploration_level
            )
            
            # Convert to API format
            api_recommendations = [
                self._convert_recommendation_to_api(rec, request.user_profile)
                for rec in recommendations
            ]
            
            # Generate user analysis
            user_analysis = self._generate_user_analysis(request.user_profile, internal_profile)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return APIRecommendationResponse(
                recommendations=api_recommendations,
                user_analysis=user_analysis,
                request_metadata={
                    "exploration_level": request.exploration_level,
                    "filters_applied": {
                        "career_fields": request.career_fields,
                        "experience_levels": request.experience_levels,
                        "salary_range": request.salary_range
                    },
                    "timestamp": datetime.now().isoformat()
                },
                total_careers_considered=len(available_careers),
                processing_time_ms=int(processing_time)
            )
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            raise
    
    def explain_recommendation(
        self, 
        user_profile: APIUserProfile, 
        career_id: str,
        exploration_level: int = 1
    ) -> Dict[str, Any]:
        """
        Get detailed explanation for a specific career recommendation.
        
        Args:
            user_profile: User's profile
            career_id: ID of the career to explain
            exploration_level: User's exploration level
            
        Returns:
            Detailed explanation of the recommendation
        """
        try:
            # Get career from database
            career_data = self.career_db.get_career(career_id)
            if not career_data:
                raise ValueError(f"Career not found: {career_id}")
            
            # Convert to internal formats
            internal_profile = self._convert_api_profile_to_internal(user_profile)
            internal_career = self._convert_career_data_to_internal(career_data)
            
            # Get explanation from engine
            explanation = self.recommendation_engine.explain_recommendation(
                internal_profile, internal_career, exploration_level
            )
            
            # Add career database information
            explanation["career_details"] = {
                "career_id": career_data.career_id,
                "title": career_data.title,
                "description": career_data.description,
                "career_field": career_data.career_field.value,
                "experience_level": career_data.experience_level.value,
                "salary_range": {
                    "min": career_data.salary_min,
                    "max": career_data.salary_max,
                    "currency": career_data.salary_currency
                },
                "required_skills": career_data.required_technical_skills + career_data.required_soft_skills,
                "learning_path": career_data.learning_path,
                "companies": career_data.companies,
                "demand_level": career_data.demand_level,
                "growth_outlook": career_data.growth_outlook
            }
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error explaining recommendation: {e}")
            raise
    
    def get_career_fields(self) -> List[Dict[str, str]]:
        """
        Get all available career fields.
        
        Returns:
            List of career field information
        """
        return [
            {"value": field.value, "label": field.value.replace("_", " ").title()}
            for field in CareerField
        ]
    
    def get_experience_levels(self) -> List[Dict[str, str]]:
        """
        Get all available experience levels.
        
        Returns:
            List of experience level information
        """
        return [
            {"value": level.value, "label": level.value.title()}
            for level in ExperienceLevel
        ]
    
    def search_careers(
        self,
        query: str,
        career_fields: Optional[List[str]] = None,
        experience_levels: Optional[List[str]] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search for careers by title or description.
        
        Args:
            query: Search query
            career_fields: Optional list of career fields to filter by
            experience_levels: Optional list of experience levels to filter by
            limit: Maximum number of results
            
        Returns:
            List of matching careers
        """
        try:
            # Convert string filters to enums
            field_filters = None
            if career_fields:
                field_filters = [CareerField(field) for field in career_fields if field in [f.value for f in CareerField]]
            
            level_filters = None
            if experience_levels:
                level_filters = [ExperienceLevel(level) for level in experience_levels if level in [l.value for l in ExperienceLevel]]
            
            # Search in database
            careers = self.career_db.search_careers(
                title_query=query,
                career_fields=field_filters,
                experience_levels=level_filters,
                limit=limit
            )
            
            # Convert to API format
            return [
                {
                    "career_id": career.career_id,
                    "title": career.title,
                    "description": career.description,
                    "career_field": career.career_field.value,
                    "experience_level": career.experience_level.value,
                    "salary_range": f"${career.salary_min:,} - ${career.salary_max:,}",
                    "required_skills": career.required_technical_skills[:5],  # Top 5 skills
                    "companies": career.companies[:3]  # Top 3 companies
                }
                for career in careers
            ]
            
        except Exception as e:
            logger.error(f"Error searching careers: {e}")
            return []
    
    def get_database_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the career database.
        
        Returns:
            Database statistics
        """
        return self.career_db.get_career_statistics()
    
    def _convert_api_profile_to_internal(self, api_profile: APIUserProfile) -> UserProfile:
        """Convert API user profile to internal UserProfile format."""
        # This is a simplified conversion - in a real implementation,
        # you would need to properly map all fields to the internal UserProfile structure
        from unittest.mock import Mock
        
        # Create a mock UserProfile for now
        # In a real implementation, you would properly construct this
        internal_profile = Mock(spec=UserProfile)
        internal_profile.user_id = api_profile.user_id
        internal_profile.technicalSkills = api_profile.technical_skills
        internal_profile.softSkills = api_profile.soft_skills
        internal_profile.experience = api_profile.experience_years
        internal_profile.industries = api_profile.industries
        internal_profile.interests = api_profile.interests
        internal_profile.careerGoals = api_profile.career_goals
        internal_profile.salaryExpectations = api_profile.salary_expectations
        internal_profile.currentRole = api_profile.current_role
        internal_profile.educationLevel = api_profile.education_level
        internal_profile.location = api_profile.location
        internal_profile.resumeText = api_profile.resume_text
        
        # Work preferences
        internal_profile.workingWithData = api_profile.working_with_data
        internal_profile.workingWithPeople = api_profile.working_with_people
        internal_profile.creativeTasks = api_profile.creative_tasks
        internal_profile.problemSolving = api_profile.problem_solving
        internal_profile.leadership = api_profile.leadership
        internal_profile.physicalHandsOnWork = api_profile.physical_hands_on_work
        internal_profile.mechanicalAptitude = api_profile.mechanical_aptitude
        
        return internal_profile
    
    def _convert_career_data_to_internal(self, career_data: CareerData):
        """Convert CareerData to internal Career format."""
        from unittest.mock import Mock
        
        # Create a mock Career for now
        internal_career = Mock()
        internal_career.career_id = career_data.career_id
        internal_career.title = career_data.title
        internal_career.description = career_data.description
        internal_career.career_field = career_data.career_field.value
        internal_career.salary_range = Mock()
        internal_career.salary_range.min = career_data.salary_min
        internal_career.salary_range.max = career_data.salary_max
        internal_career.salary_range.currency = career_data.salary_currency
        internal_career.required_skills = []  # Would need proper Skill objects
        
        return internal_career
    
    def _get_filtered_careers(self, request: APIRecommendationRequest) -> List:
        """Get careers from database with applied filters."""
        # Convert string filters to enums
        field_filters = None
        if request.career_fields:
            field_filters = [
                CareerField(field) for field in request.career_fields 
                if field in [f.value for f in CareerField]
            ]
        
        level_filters = None
        if request.experience_levels:
            level_filters = [
                ExperienceLevel(level) for level in request.experience_levels 
                if level in [l.value for l in ExperienceLevel]
            ]
        
        # Get salary filters
        salary_min = None
        salary_max = None
        if request.salary_range:
            salary_min = request.salary_range.get("min")
            salary_max = request.salary_range.get("max")
        
        # Search careers
        career_data_list = self.career_db.search_careers(
            career_fields=field_filters,
            experience_levels=level_filters,
            salary_min=salary_min,
            salary_max=salary_max,
            limit=1000  # Large limit for initial filtering
        )
        
        # Convert to internal format
        return [self._convert_career_data_to_internal(cd) for cd in career_data_list]
    
    def _convert_recommendation_to_api(
        self, 
        recommendation: CareerRecommendation, 
        user_profile: APIUserProfile
    ) -> APICareerRecommendation:
        """Convert internal recommendation to API format."""
        # Get career data from database
        career_data = self.career_db.get_career(recommendation.career.career_id)
        if not career_data:
            # Fallback to recommendation data
            career_data = CareerData(
                career_id=recommendation.career.career_id,
                title=recommendation.career.title,
                description=recommendation.career.description,
                career_field=CareerField.OTHER,
                experience_level=ExperienceLevel.MID,
                salary_min=50000,
                salary_max=100000
            )
        
        # Generate field analysis
        user_field, user_confidence = determine_enhanced_user_career_field(
            self._convert_api_profile_to_internal(user_profile)
        )
        career_field, career_confidence = get_enhanced_career_field(recommendation.career)
        
        return APICareerRecommendation(
            career_id=career_data.career_id,
            title=career_data.title,
            description=career_data.description,
            career_field=career_data.career_field.value,
            experience_level=career_data.experience_level.value,
            salary_min=career_data.salary_min,
            salary_max=career_data.salary_max,
            salary_currency=career_data.salary_currency,
            relevance_score=recommendation.score.total_score,
            confidence_level=recommendation.confidence,
            category=recommendation.category.value if hasattr(recommendation.category, 'value') else str(recommendation.category),
            match_reasons=recommendation.reasons,
            skill_analysis={
                "matched_skills": recommendation.score.breakdown.get("skill_details", {}).get("matched_skills", []),
                "missing_skills": recommendation.score.breakdown.get("skill_details", {}).get("missing_mandatory", []),
                "skill_match_score": recommendation.score.skill_match_score
            },
            field_analysis={
                "user_field": user_field,
                "career_field": career_field,
                "field_transition": "same_field" if user_field == career_field else "field_change",
                "user_field_confidence": user_confidence,
                "career_field_confidence": career_confidence
            },
            required_skills=career_data.required_technical_skills + career_data.required_soft_skills,
            learning_path=career_data.learning_path,
            companies=career_data.companies,
            work_environment=career_data.work_environments,
            remote_options=career_data.remote_options,
            demand_level=career_data.demand_level,
            growth_outlook=career_data.growth_outlook
        )
    
    def _generate_user_analysis(self, api_profile: APIUserProfile, internal_profile) -> Dict[str, Any]:
        """Generate analysis of the user's profile."""
        user_field, user_confidence = determine_enhanced_user_career_field(internal_profile)
        
        return {
            "primary_career_field": user_field,
            "field_confidence": user_confidence,
            "experience_summary": {
                "years": api_profile.experience_years,
                "current_role": api_profile.current_role,
                "education_level": api_profile.education_level
            },
            "skill_summary": {
                "technical_skills_count": len(api_profile.technical_skills),
                "soft_skills_count": len(api_profile.soft_skills),
                "certifications_count": len(api_profile.certifications),
                "top_technical_skills": api_profile.technical_skills[:5]
            },
            "work_preferences": {
                "data_oriented": api_profile.working_with_data >= 4,
                "people_oriented": api_profile.working_with_people >= 4,
                "creative_oriented": api_profile.creative_tasks >= 4,
                "leadership_oriented": api_profile.leadership >= 4,
                "hands_on_oriented": api_profile.physical_hands_on_work >= 4
            },
            "career_focus": {
                "industries": api_profile.industries,
                "interests": api_profile.interests,
                "goals": api_profile.career_goals
            }
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize API
    api = UnifiedRecommendationAPI("test_unified_careers.db")
    
    # Create sample user profile
    user_profile = APIUserProfile(
        user_id="test_user_001",
        current_role="Senior Product Manager",
        experience_years=8.0,
        education_level="masters",
        technical_skills=["Product Management", "Data Analysis", "Strategic Planning"],
        soft_skills=["Leadership", "Communication", "Problem Solving"],
        working_with_data=4,
        working_with_people=5,
        creative_tasks=4,
        problem_solving=5,
        leadership=5,
        interests=["Technology", "Business Strategy", "Innovation"],
        industries=["Technology & Software", "Financial Services"],
        career_goals="Advance to executive leadership role",
        salary_expectations={"min": 150000, "max": 250000, "currency": "USD"}
    )
    
    # Create recommendation request
    request = APIRecommendationRequest(
        user_profile=user_profile,
        exploration_level=2,  # Stretch zone
        limit=5
    )
    
    print("Unified API initialized successfully!")
    print(f"Available career fields: {len(api.get_career_fields())}")
    print(f"Available experience levels: {len(api.get_experience_levels())}")
    print(f"Database statistics: {api.get_database_statistics()}")