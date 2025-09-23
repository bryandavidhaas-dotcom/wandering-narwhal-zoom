"""
Enhanced categorization logic for the recommendation engine.

This module implements an improved categorization system that addresses the issues
with the rigid keyword-based approach. It includes context-aware career field
determination and better handling of seniority levels and role relationships.
"""

from typing import List, Dict, Optional, Tuple, Set
import re
from dataclasses import dataclass
from models import (
    Career, RecommendationScore, CareerRecommendation,
    RecommendationCategory, UserProfile
)
from config import CategorizationThresholds


@dataclass
class CareerFieldMapping:
    """Enhanced career field mapping with context awareness."""
    primary_keywords: List[str]
    secondary_keywords: List[str]
    exclusion_keywords: List[str]
    seniority_indicators: List[str]
    related_fields: List[str]
    weight: float = 1.0


# Enhanced career field categories with context awareness
ENHANCED_CAREER_FIELD_CATEGORIES = {
    'technology': CareerFieldMapping(
        primary_keywords=[
            'software engineer', 'developer', 'programmer', 'data scientist', 'data analyst',
            'machine learning', 'artificial intelligence', 'cybersecurity', 'devops', 'cloud',
            'database administrator', 'systems administrator', 'network engineer', 'it support',
            'technical writer', 'qa engineer', 'mobile developer', 'web developer', 
            'full stack', 'frontend', 'backend', 'software architect', 'platform engineer'
        ],
        secondary_keywords=[
            'product manager', 'scrum master', 'agile', 'ui/ux designer', 'user experience', 
            'user interface', 'technical lead', 'engineering manager'
        ],
        exclusion_keywords=[
            'chief', 'vp', 'vice president', 'svp', 'senior vice president', 'ceo', 'cto',
            'director', 'head of', 'executive'
        ],
        seniority_indicators=[
            'junior', 'senior', 'lead', 'principal', 'staff', 'manager', 'director'
        ],
        related_fields=['business_finance', 'creative_arts'],
        weight=1.0
    ),
    
    'business_finance': CareerFieldMapping(
        primary_keywords=[
            'business analyst', 'financial analyst', 'accountant', 'controller', 'cfo',
            'investment banker', 'financial advisor', 'portfolio manager', 'risk analyst',
            'management consultant', 'strategy consultant', 'operations manager',
            'business development', 'corporate finance', 'treasury', 'market research', 
            'business intelligence', 'financial planner', 'auditor'
        ],
        secondary_keywords=[
            'project manager', 'program manager', 'product manager'
        ],
        exclusion_keywords=[],
        seniority_indicators=[
            'junior', 'senior', 'lead', 'principal', 'manager', 'director', 'vp', 'svp', 'chief'
        ],
        related_fields=['technology', 'sales_marketing'],
        weight=1.0
    ),
    
    'executive_leadership': CareerFieldMapping(
        primary_keywords=[
            'ceo', 'chief executive officer', 'cto', 'chief technology officer', 
            'cfo', 'chief financial officer', 'coo', 'chief operating officer',
            'president', 'vice president', 'vp', 'svp', 'senior vice president',
            'executive director', 'managing director', 'general manager'
        ],
        secondary_keywords=[
            'head of', 'director of', 'senior director'
        ],
        exclusion_keywords=[],
        seniority_indicators=[
            'c-level', 'executive', 'senior executive', 'chief', 'president', 'vp'
        ],
        related_fields=['business_finance', 'technology', 'sales_marketing'],
        weight=2.0  # Higher weight for executive roles
    ),
    
    'sales_marketing': CareerFieldMapping(
        primary_keywords=[
            'sales representative', 'account executive', 'sales manager', 'business development',
            'marketing coordinator', 'marketing manager', 'digital marketing specialist',
            'social media manager', 'content creator', 'copywriter', 'brand manager',
            'public relations', 'communications specialist', 'advertising', 'seo specialist',
            'email marketing', 'growth marketing', 'product marketing', 'event coordinator',
            'customer success', 'account manager', 'inside sales', 'outside sales'
        ],
        secondary_keywords=[],
        exclusion_keywords=[],
        seniority_indicators=[
            'junior', 'senior', 'lead', 'manager', 'director', 'vp', 'head of'
        ],
        related_fields=['business_finance', 'creative_arts'],
        weight=1.0
    ),
    
    'healthcare': CareerFieldMapping(
        primary_keywords=[
            'physician', 'doctor', 'nurse', 'registered nurse', 'nurse practitioner',
            'physician assistant', 'medical assistant', 'pharmacist', 'pharmacy technician',
            'physical therapist', 'occupational therapist', 'respiratory therapist',
            'medical technologist', 'radiologic technologist', 'dental hygienist',
            'healthcare administrator', 'medical coder', 'health information', 'clinical',
            'surgeon', 'anesthesiologist', 'cardiologist', 'dermatologist', 'psychiatrist'
        ],
        secondary_keywords=[],
        exclusion_keywords=[],
        seniority_indicators=[
            'junior', 'senior', 'lead', 'chief', 'head', 'director'
        ],
        related_fields=['technology'],
        weight=1.5  # Higher weight due to specialization
    ),
    
    'government_public_service': CareerFieldMapping(
        primary_keywords=[
            'policy analyst', 'government relations specialist', 'public affairs manager',
            'regulatory affairs specialist', 'city planner', 'public administrator',
            'legislative director', 'congressional staff director', 'senior executive service',
            'legislative analyst', 'government analyst', 'public policy', 'civil service',
            'municipal', 'county', 'diplomat', 'police chief', 'fire chief', 'sheriff'
        ],
        secondary_keywords=[
            'federal', 'state', 'gs-'
        ],
        exclusion_keywords=[],
        seniority_indicators=[
            'junior', 'senior', 'lead', 'chief', 'director', 'commissioner'
        ],
        related_fields=['legal_law', 'business_finance'],
        weight=1.2
    ),
    
    'legal_law': CareerFieldMapping(
        primary_keywords=[
            'lawyer', 'attorney', 'paralegal', 'legal assistant', 'judge', 'magistrate',
            'legal counsel', 'corporate counsel', 'public defender', 'prosecutor',
            'legal researcher', 'court reporter', 'legal secretary', 'compliance officer',
            'contract specialist', 'intellectual property', 'patent attorney'
        ],
        secondary_keywords=[],
        exclusion_keywords=[],
        seniority_indicators=[
            'junior', 'senior', 'lead', 'chief', 'head', 'general counsel'
        ],
        related_fields=['government_public_service', 'business_finance'],
        weight=1.3
    ),
    
    'education': CareerFieldMapping(
        primary_keywords=[
            'teacher', 'professor', 'instructor', 'tutor', 'principal', 'administrator',
            'curriculum developer', 'instructional designer', 'education coordinator',
            'academic advisor', 'librarian', 'school counselor', 'special education',
            'early childhood education', 'elementary teacher', 'secondary teacher',
            'higher education', 'training specialist', 'corporate trainer'
        ],
        secondary_keywords=[],
        exclusion_keywords=[],
        seniority_indicators=[
            'assistant', 'associate', 'full', 'head', 'dean', 'provost'
        ],
        related_fields=['technology', 'creative_arts'],
        weight=1.0
    ),
    
    'skilled_trades': CareerFieldMapping(
        primary_keywords=[
            'electrician', 'plumber', 'carpenter', 'mechanic', 'technician', 'welder',
            'hvac technician', 'automotive technician', 'aircraft mechanic', 'maintenance',
            'construction worker', 'contractor', 'installer', 'repair technician',
            'machinist', 'tool and die maker', 'millwright', 'pipefitter', 'roofer',
            'painter', 'mason', 'heavy equipment operator'
        ],
        secondary_keywords=[],
        exclusion_keywords=[],
        seniority_indicators=[
            'apprentice', 'journeyman', 'master', 'lead', 'supervisor', 'foreman'
        ],
        related_fields=['manufacturing_industrial'],
        weight=1.0
    ),
    
    'creative_arts': CareerFieldMapping(
        primary_keywords=[
            'graphic designer', 'artist', 'photographer', 'videographer', 'animator',
            'writer', 'editor', 'journalist', 'content creator', 'creative director',
            'art director', 'musician', 'actor', 'producer', 'director', 'designer',
            'illustrator', 'web designer', 'fashion designer', 'interior designer'
        ],
        secondary_keywords=[],
        exclusion_keywords=[],
        seniority_indicators=[
            'junior', 'senior', 'lead', 'principal', 'creative director', 'art director'
        ],
        related_fields=['technology', 'sales_marketing'],
        weight=1.0
    ),
    
    'hospitality_service': CareerFieldMapping(
        primary_keywords=[
            'hotel manager', 'restaurant manager', 'chef', 'cook', 'server', 'bartender',
            'tourism director', 'tourism manager', 'travel agent', 'event planner',
            'hospitality', 'customer service', 'retail manager', 'spa manager',
            'recreation coordinator', 'tour guide', 'concierge'
        ],
        secondary_keywords=[],
        exclusion_keywords=[],
        seniority_indicators=[
            'assistant', 'senior', 'lead', 'manager', 'director', 'general manager'
        ],
        related_fields=['sales_marketing'],
        weight=1.0
    ),
    
    'agriculture_environment': CareerFieldMapping(
        primary_keywords=[
            'farmer', 'agricultural specialist', 'environmental scientist', 'forester',
            'conservation director', 'conservation manager', 'environmental director',
            'environmental manager', 'sustainability', 'organic farm', 'ranch manager',
            'agricultural engineer', 'soil scientist', 'wildlife biologist', 'park ranger'
        ],
        secondary_keywords=[],
        exclusion_keywords=[],
        seniority_indicators=[
            'junior', 'senior', 'lead', 'manager', 'director', 'chief'
        ],
        related_fields=['technology', 'government_public_service'],
        weight=1.0
    ),
    
    'manufacturing_industrial': CareerFieldMapping(
        primary_keywords=[
            'production manager', 'quality control', 'manufacturing engineer',
            'industrial engineer', 'plant manager', 'operations supervisor',
            'assembly worker', 'machine operator', 'warehouse manager',
            'logistics coordinator', 'supply chain', 'inventory manager'
        ],
        secondary_keywords=[],
        exclusion_keywords=[],
        seniority_indicators=[
            'junior', 'senior', 'lead', 'supervisor', 'manager', 'director'
        ],
        related_fields=['skilled_trades', 'technology'],
        weight=1.0
    )
}


def extract_seniority_level(career_title: str) -> str:
    """
    Extract seniority level from career title.
    
    Args:
        career_title: Career title to analyze
        
    Returns:
        Seniority level string
    """
    title_lower = career_title.lower()
    
    # Executive level indicators
    executive_indicators = [
        'ceo', 'cto', 'cfo', 'coo', 'chief', 'president', 'vp', 'vice president',
        'svp', 'senior vice president', 'executive director', 'managing director'
    ]
    
    # Senior level indicators
    senior_indicators = [
        'director', 'head of', 'senior director', 'principal', 'lead', 'senior'
    ]
    
    # Mid level indicators
    mid_indicators = [
        'manager', 'supervisor', 'coordinator', 'specialist'
    ]
    
    # Junior level indicators
    junior_indicators = [
        'junior', 'associate', 'assistant', 'entry', 'trainee', 'intern'
    ]
    
    for indicator in executive_indicators:
        if indicator in title_lower:
            return 'executive'
    
    for indicator in senior_indicators:
        if indicator in title_lower:
            return 'senior'
    
    for indicator in mid_indicators:
        if indicator in title_lower:
            return 'mid'
    
    for indicator in junior_indicators:
        if indicator in title_lower:
            return 'junior'
    
    return 'mid'  # Default to mid-level


def get_enhanced_career_field(career: Career) -> Tuple[str, float]:
    """
    Determine the career field using enhanced context-aware categorization.
    
    Args:
        career: Career object to categorize
        
    Returns:
        Tuple of (career_field, confidence_score)
    """
    if career.career_field and career.career_field != 'other':
        return career.career_field, 1.0
    
    career_text = (career.title + " " + career.description).lower()
    career_title = career.title.lower()
    
    field_scores = {}
    
    for field, mapping in ENHANCED_CAREER_FIELD_CATEGORIES.items():
        score = 0.0
        
        # Check primary keywords (high weight)
        for keyword in mapping.primary_keywords:
            if keyword in career_text:
                # Exact title match gets highest score
                if keyword in career_title:
                    score += 3.0 * mapping.weight
                else:
                    score += 2.0 * mapping.weight
        
        # Check secondary keywords (medium weight)
        for keyword in mapping.secondary_keywords:
            if keyword in career_text:
                if keyword in career_title:
                    score += 2.0 * mapping.weight
                else:
                    score += 1.0 * mapping.weight
        
        # Apply exclusion penalties
        for exclusion in mapping.exclusion_keywords:
            if exclusion in career_title:
                # If this is an executive role, boost executive_leadership field
                if field == 'executive_leadership':
                    score += 4.0 * mapping.weight
                else:
                    # Penalize other fields for executive titles
                    score -= 2.0
        
        # Seniority context bonus
        seniority = extract_seniority_level(career.title)
        if seniority in ['executive'] and field == 'executive_leadership':
            score += 3.0
        elif seniority in mapping.seniority_indicators:
            score += 0.5
        
        field_scores[field] = max(0, score)
    
    if not field_scores or max(field_scores.values()) == 0:
        return 'other', 0.0
    
    best_field = max(field_scores, key=field_scores.get)
    confidence = min(1.0, field_scores[best_field] / 5.0)  # Normalize to 0-1
    
    return best_field, confidence


def determine_enhanced_user_career_field(user_profile: UserProfile) -> Tuple[str, float]:
    """
    Determine the user's primary career field using enhanced analysis.
    
    Args:
        user_profile: User's profile with career information
        
    Returns:
        Tuple of (primary_career_field, confidence_score)
    """
    text_sources = []
    
    # Collect text sources with weights
    weighted_sources = []
    
    # Current role (highest weight)
    if hasattr(user_profile, 'professional_data') and user_profile.professional_data:
        for exp in user_profile.professional_data.experience:
            weighted_sources.append((exp.title.lower(), 3.0))
            text_sources.append(exp.title.lower())
    
    # Skills (medium weight)
    if user_profile.skills:
        for skill in user_profile.skills:
            weighted_sources.append((skill.name.lower(), 1.5))
            text_sources.append(skill.name.lower())
    
    # Resume skills (medium weight)
    if hasattr(user_profile, 'professional_data') and user_profile.professional_data:
        if user_profile.professional_data.resume_skills:
            for skill in user_profile.professional_data.resume_skills:
                weighted_sources.append((skill.lower(), 1.5))
                text_sources.append(skill.lower())
    
    combined_text = " ".join(text_sources)
    
    # Score each career field
    field_scores = {}
    for field, mapping in ENHANCED_CAREER_FIELD_CATEGORIES.items():
        score = 0.0
        
        # Check weighted sources
        for text, weight in weighted_sources:
            for keyword in mapping.primary_keywords:
                if keyword in text:
                    score += weight * mapping.weight
            
            for keyword in mapping.secondary_keywords:
                if keyword in text:
                    score += (weight * 0.7) * mapping.weight
        
        field_scores[field] = score
    
    if not field_scores or max(field_scores.values()) == 0:
        return 'other', 0.0
    
    best_field = max(field_scores, key=field_scores.get)
    total_score = sum(field_scores.values())
    confidence = field_scores[best_field] / total_score if total_score > 0 else 0.0
    
    return best_field, min(1.0, confidence)


class EnhancedCategorizationEngine:
    """
    Enhanced categorization engine with improved career field detection
    and context-aware recommendation categorization.
    """
    
    def __init__(self, thresholds: CategorizationThresholds):
        """
        Initialize the enhanced categorization engine.
        
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
        Categorize career recommendations using enhanced logic.
        
        Args:
            user_profile: User's profile for context
            careers: List of careers being recommended
            scores: Corresponding recommendation scores
            
        Returns:
            List of CareerRecommendation objects with enhanced categories and reasons
        """
        career_dict = {career.career_id: career for career in careers}
        recommendations = []
        
        # Get user's career field for context
        user_field, user_field_confidence = determine_enhanced_user_career_field(user_profile)
        
        for score in scores:
            career = career_dict.get(score.career_id)
            if not career:
                continue
            
            # Get career field with confidence
            career_field, career_field_confidence = get_enhanced_career_field(career)
            
            category = self._determine_enhanced_category(
                score, user_profile, career, user_field, career_field
            )
            reasons = self._generate_enhanced_reasons(
                score, user_profile, career, category, user_field, career_field
            )
            confidence = self._calculate_enhanced_confidence(
                score, category, user_field_confidence, career_field_confidence
            )
            
            recommendation = CareerRecommendation(
                career=career,
                score=score,
                category=category,
                reasons=reasons,
                confidence=confidence
            )
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _determine_enhanced_category(
        self, 
        score: RecommendationScore, 
        user_profile: UserProfile, 
        career: Career,
        user_field: str,
        career_field: str
    ) -> RecommendationCategory:
        """
        Determine category using enhanced logic that considers field transitions.
        """
        total_score = score.total_score
        skill_score = score.skill_match_score
        
        # Extract seniority levels
        user_seniority = self._get_user_seniority_level(user_profile)
        career_seniority = extract_seniority_level(career.title)
        
        # Field transition analysis
        same_field = user_field == career_field
        related_fields = career_field in ENHANCED_CAREER_FIELD_CATEGORIES.get(user_field, CareerFieldMapping([], [], [], [], [])).related_fields
        
        # Seniority transition analysis
        seniority_levels = ['junior', 'mid', 'senior', 'executive']
        user_seniority_idx = seniority_levels.index(user_seniority) if user_seniority in seniority_levels else 1
        career_seniority_idx = seniority_levels.index(career_seniority) if career_seniority in seniority_levels else 1
        seniority_gap = career_seniority_idx - user_seniority_idx
        
        # Enhanced categorization logic
        if total_score >= self.thresholds.safe_zone_min:
            if same_field and seniority_gap <= 1 and skill_score >= 0.7:
                return RecommendationCategory.SAFE_ZONE
            elif (same_field or related_fields) and seniority_gap <= 2:
                return RecommendationCategory.STRETCH_ZONE
            else:
                return RecommendationCategory.ADVENTURE_ZONE
                
        elif total_score >= self.thresholds.stretch_zone_min:
            if same_field and seniority_gap <= 0:
                return RecommendationCategory.SAFE_ZONE
            elif same_field or related_fields:
                return RecommendationCategory.STRETCH_ZONE
            else:
                return RecommendationCategory.ADVENTURE_ZONE
                
        else:
            # Lower scores are generally adventure zone, but consider field alignment
            if same_field and seniority_gap <= -1:  # Step down in seniority
                return RecommendationCategory.STRETCH_ZONE
            else:
                return RecommendationCategory.ADVENTURE_ZONE
    
    def _get_user_seniority_level(self, user_profile: UserProfile) -> str:
        """Extract user's seniority level from their profile."""
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
    
    def _generate_enhanced_reasons(
        self, 
        score: RecommendationScore, 
        user_profile: UserProfile, 
        career: Career,
        category: RecommendationCategory,
        user_field: str,
        career_field: str
    ) -> List[str]:
        """Generate enhanced reasons that include field transition context."""
        reasons = []
        
        # Field transition reasons
        if user_field == career_field:
            reasons.append(f"Stays within your {user_field.replace('_', ' ')} expertise")
        elif career_field in ENHANCED_CAREER_FIELD_CATEGORIES.get(user_field, CareerFieldMapping([], [], [], [], [])).related_fields:
            reasons.append(f"Natural transition from {user_field.replace('_', ' ')} to {career_field.replace('_', ' ')}")
        else:
            reasons.append(f"Opportunity to explore {career_field.replace('_', ' ')} field")
        
        # Seniority reasons
        user_seniority = self._get_user_seniority_level(user_profile)
        career_seniority = extract_seniority_level(career.title)
        
        if user_seniority == career_seniority:
            reasons.append("Matches your current seniority level")
        elif career_seniority == 'executive' and user_seniority == 'senior':
            reasons.append("Executive advancement opportunity")
        elif career_seniority == 'senior' and user_seniority == 'mid':
            reasons.append("Senior-level growth opportunity")
        
        # Skill-based reasons (enhanced)
        if score.skill_match_score >= 0.8:
            matched_skills = score.breakdown.get("skill_details", {}).get("matched_skills", [])
            if matched_skills:
                skill_names = [skill["name"] for skill in matched_skills[:3]]
                reasons.append(f"Strong skill alignment: {', '.join(skill_names)}")
        elif score.skill_match_score >= 0.5:
            reasons.append("Good foundation with transferable skills")
        else:
            reasons.append("Opportunity to develop new expertise")
        
        # Category-specific enhanced reasons
        if category == RecommendationCategory.SAFE_ZONE:
            reasons.append("Low-risk transition with high success probability")
        elif category == RecommendationCategory.STRETCH_ZONE:
            reasons.append("Achievable growth opportunity with moderate effort")
        elif category == RecommendationCategory.ADVENTURE_ZONE:
            reasons.append("Bold career pivot with significant learning potential")
        
        return reasons[:5]  # Limit to top 5 reasons
    
    def _calculate_enhanced_confidence(
        self, 
        score: RecommendationScore, 
        category: RecommendationCategory,
        user_field_confidence: float,
        career_field_confidence: float
    ) -> float:
        """Calculate confidence with field classification confidence factored in."""
        base_confidence = score.total_score
        
        # Factor in field classification confidence
        field_confidence_factor = (user_field_confidence + career_field_confidence) / 2
        
        # Adjust based on category
        if category == RecommendationCategory.SAFE_ZONE:
            confidence = min(1.0, base_confidence + 0.1)
        elif category == RecommendationCategory.STRETCH_ZONE:
            confidence = base_confidence
        else:  # ADVENTURE_ZONE
            confidence = max(0.3, base_confidence - 0.1)
        
        # Apply field confidence factor
        final_confidence = confidence * (0.7 + 0.3 * field_confidence_factor)
        
        return min(1.0, max(0.1, final_confidence))