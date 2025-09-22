"""
Categorization logic for the recommendation engine.

This module implements the logic to categorize scored career recommendations
into Safe Zone, Stretch Zone, and Adventure Zone based on configurable thresholds.
It also includes career field categorization and user profile analysis.
"""

from typing import List, Dict, Optional
from .models import (
    Career, RecommendationScore, CareerRecommendation,
    RecommendationCategory, UserProfile
)
from .config import CategorizationThresholds


# Standardized career field categories
CAREER_FIELD_CATEGORIES = {
    'technology': [
        'software engineer', 'developer', 'programmer', 'data scientist', 'data analyst',
        'machine learning', 'artificial intelligence', 'cybersecurity', 'devops', 'cloud',
        'database administrator', 'systems administrator', 'network engineer', 'it support',
        'technical writer', 'product manager', 'scrum master', 'agile', 'qa engineer',
        'mobile developer', 'web developer', 'full stack', 'frontend', 'backend',
        'ui/ux designer', 'user experience', 'user interface', 'software architect'
    ],
    
    'business_finance': [
        'business analyst', 'financial analyst', 'accountant', 'controller', 'cfo',
        'investment banker', 'financial advisor', 'portfolio manager', 'risk analyst',
        'management consultant', 'strategy consultant', 'operations manager',
        'project manager', 'business development', 'corporate finance', 'treasury',
        'market research', 'business intelligence', 'financial planner', 'auditor'
    ],
    
    'sales_marketing': [
        'sales representative', 'account executive', 'sales manager', 'business development',
        'marketing coordinator', 'marketing manager', 'digital marketing specialist',
        'social media manager', 'content creator', 'copywriter', 'brand manager',
        'public relations', 'communications specialist', 'advertising', 'seo specialist',
        'email marketing', 'growth marketing', 'product marketing', 'event coordinator',
        'customer success', 'account manager', 'inside sales', 'outside sales'
    ],
    
    'healthcare': [
        'physician', 'doctor', 'nurse', 'registered nurse', 'nurse practitioner',
        'physician assistant', 'medical assistant', 'pharmacist', 'pharmacy technician',
        'physical therapist', 'occupational therapist', 'respiratory therapist',
        'medical technologist', 'radiologic technologist', 'dental hygienist',
        'healthcare administrator', 'medical coder', 'health information', 'clinical',
        'surgeon', 'anesthesiologist', 'cardiologist', 'dermatologist', 'psychiatrist'
    ],
    
    'education': [
        'teacher', 'professor', 'instructor', 'tutor', 'principal', 'administrator',
        'curriculum developer', 'instructional designer', 'education coordinator',
        'academic advisor', 'librarian', 'school counselor', 'special education',
        'early childhood education', 'elementary teacher', 'secondary teacher',
        'higher education', 'training specialist', 'corporate trainer'
    ],
    
    'skilled_trades': [
        'electrician', 'plumber', 'carpenter', 'mechanic', 'technician', 'welder',
        'hvac technician', 'automotive technician', 'aircraft mechanic', 'maintenance',
        'construction worker', 'contractor', 'installer', 'repair technician',
        'machinist', 'tool and die maker', 'millwright', 'pipefitter', 'roofer',
        'painter', 'mason', 'heavy equipment operator'
    ],
    
    'government_public_service': [
        'policy analyst', 'government relations specialist', 'public affairs manager',
        'regulatory affairs specialist', 'city planner', 'public administrator',
        'legislative director', 'congressional staff director', 'senior executive service',
        'legislative analyst', 'government analyst', 'federal', 'state', 'gs-',
        'public policy', 'civil service', 'municipal', 'county', 'diplomat'
    ],
    
    'legal_law': [
        'lawyer', 'attorney', 'paralegal', 'legal assistant', 'judge', 'magistrate',
        'legal counsel', 'corporate counsel', 'public defender', 'prosecutor',
        'legal researcher', 'court reporter', 'legal secretary', 'compliance officer',
        'contract specialist', 'intellectual property', 'patent attorney'
    ],
    
    'creative_arts': [
        'graphic designer', 'artist', 'photographer', 'videographer', 'animator',
        'writer', 'editor', 'journalist', 'content creator', 'creative director',
        'art director', 'musician', 'actor', 'producer', 'director', 'designer',
        'illustrator', 'web designer', 'fashion designer', 'interior designer'
    ],
    
    'hospitality_service': [
        'hotel manager', 'restaurant manager', 'chef', 'cook', 'server', 'bartender',
        'tourism director', 'tourism manager', 'travel agent', 'event planner',
        'hospitality', 'customer service', 'retail manager', 'spa manager',
        'recreation coordinator', 'tour guide', 'concierge'
    ],
    
    'agriculture_environment': [
        'farmer', 'agricultural specialist', 'environmental scientist', 'forester',
        'conservation director', 'conservation manager', 'environmental director',
        'environmental manager', 'sustainability', 'organic farm', 'ranch manager',
        'agricultural engineer', 'soil scientist', 'wildlife biologist', 'park ranger'
    ],
    
    'manufacturing_industrial': [
        'production manager', 'quality control', 'manufacturing engineer',
        'industrial engineer', 'plant manager', 'operations supervisor',
        'assembly worker', 'machine operator', 'warehouse manager',
        'logistics coordinator', 'supply chain', 'inventory manager'
    ]
}


def get_career_field(career: Career) -> str:
    """
    Determine the career field for a given career.
    
    Args:
        career: Career object to categorize
        
    Returns:
        Career field category string
    """
    if career.career_field:
        return career.career_field
    
    # Fallback to keyword-based categorization
    career_text = (career.title + " " + career.description).lower()
    
    for field, keywords in CAREER_FIELD_CATEGORIES.items():
        for keyword in keywords:
            if keyword in career_text:
                return field
    
    return 'other'


def determine_user_career_field(user_profile: UserProfile) -> str:
    """
    Determine the user's primary career field based on their profile.
    
    This function analyzes the user's current role, resume text, and technical skills
    to infer their primary career field by matching keywords against the defined
    career field categories.
    
    Args:
        user_profile: User's profile with career information
        
    Returns:
        Primary career field category string
    """
    # Collect all text sources for analysis
    text_sources = []
    
    # Add current role
    if hasattr(user_profile, 'professional_data') and user_profile.professional_data:
        for exp in user_profile.professional_data.experience:
            text_sources.append(exp.title.lower())
    
    # Add resume text if available
    if hasattr(user_profile, 'professional_data') and user_profile.professional_data:
        if user_profile.professional_data.resume_skills:
            text_sources.extend([skill.lower() for skill in user_profile.professional_data.resume_skills])
    
    # Add technical skills
    if user_profile.skills:
        text_sources.extend([skill.name.lower() for skill in user_profile.skills])
    
    # Combine all text for analysis
    combined_text = " ".join(text_sources)
    
    # Score each career field based on keyword matches
    field_scores = {}
    for field, keywords in CAREER_FIELD_CATEGORIES.items():
        score = 0
        for keyword in keywords:
            if keyword in combined_text:
                # Weight longer keywords more heavily
                score += len(keyword.split())
        field_scores[field] = score
    
    # Return the field with the highest score
    if field_scores and max(field_scores.values()) > 0:
        return max(field_scores, key=field_scores.get)
    
    return 'other'


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