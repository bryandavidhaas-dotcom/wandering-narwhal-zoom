"""
Tests for the enhanced categorization system.

This module tests the improved categorization logic that addresses the issues
with inappropriate recommendations like "SVP of Product" → "Police Chief".
"""

import pytest
from unittest.mock import Mock
from recommendation_engine.enhanced_categorization import (
    get_enhanced_career_field,
    determine_enhanced_user_career_field,
    extract_seniority_level,
    EnhancedCategorizationEngine,
    ENHANCED_CAREER_FIELD_CATEGORIES
)
from recommendation_engine.models import Career, UserProfile, RecommendationScore, RecommendationCategory
from recommendation_engine.config import CategorizationThresholds


class TestEnhancedCareerFieldDetection:
    """Test enhanced career field detection logic."""
    
    def test_executive_role_detection(self):
        """Test that executive roles are properly categorized."""
        # Create mock career for SVP of Product
        svp_career = Mock(spec=Career)
        svp_career.career_field = None
        svp_career.title = "Senior Vice President of Product Management"
        svp_career.description = "Lead product strategy and management across multiple product lines"
        
        field, confidence = get_enhanced_career_field(svp_career)
        
        assert field == 'executive_leadership'
        assert confidence > 0.8
    
    def test_police_chief_detection(self):
        """Test that police chief is properly categorized as government/public service."""
        police_career = Mock(spec=Career)
        police_career.career_field = None
        police_career.title = "Police Chief"
        police_career.description = "Lead law enforcement operations and public safety initiatives"
        
        field, confidence = get_enhanced_career_field(police_career)
        
        assert field == 'government_public_service'
        assert confidence > 0.7
    
    def test_product_manager_vs_executive_distinction(self):
        """Test that regular product managers are not confused with executives."""
        # Regular Product Manager
        pm_career = Mock(spec=Career)
        pm_career.career_field = None
        pm_career.title = "Product Manager"
        pm_career.description = "Manage product roadmap and work with engineering teams"
        
        pm_field, pm_confidence = get_enhanced_career_field(pm_career)
        
        # Senior VP of Product
        svp_career = Mock(spec=Career)
        svp_career.career_field = None
        svp_career.title = "Senior Vice President of Product"
        svp_career.description = "Executive leadership of product organization"
        
        svp_field, svp_confidence = get_enhanced_career_field(svp_career)
        
        # They should be in different fields
        assert pm_field == 'technology'  # Secondary keyword match
        assert svp_field == 'executive_leadership'  # Executive role
        assert pm_field != svp_field


class TestSeniorityExtraction:
    """Test seniority level extraction from job titles."""
    
    def test_executive_seniority_detection(self):
        """Test detection of executive-level roles."""
        executive_titles = [
            "Chief Executive Officer",
            "CEO",
            "Senior Vice President of Product",
            "SVP Marketing",
            "President of Engineering",
            "Managing Director"
        ]
        
        for title in executive_titles:
            seniority = extract_seniority_level(title)
            assert seniority == 'executive', f"Failed for title: {title}"
    
    def test_senior_seniority_detection(self):
        """Test detection of senior-level roles."""
        senior_titles = [
            "Director of Engineering",
            "Senior Director of Product",
            "Head of Marketing",
            "Principal Engineer",
            "Lead Data Scientist"
        ]
        
        for title in senior_titles:
            seniority = extract_seniority_level(title)
            assert seniority == 'senior', f"Failed for title: {title}"
    
    def test_mid_seniority_detection(self):
        """Test detection of mid-level roles."""
        mid_titles = [
            "Product Manager",
            "Engineering Manager",
            "Marketing Specialist",
            "Data Scientist",
            "Software Engineer"
        ]
        
        for title in mid_titles:
            seniority = extract_seniority_level(title)
            assert seniority == 'mid', f"Failed for title: {title}"


class TestUserCareerFieldDetection:
    """Test user career field detection from profile."""
    
    def test_executive_user_detection(self):
        """Test that executive users are properly identified."""
        # Mock user profile for SVP of Product
        user_profile = Mock(spec=UserProfile)
        user_profile.professional_data = Mock()
        user_profile.professional_data.experience = [
            Mock(title="Senior Vice President of Product Management", duration_years=3),
            Mock(title="VP Product", duration_years=4),
            Mock(title="Director of Product", duration_years=5)
        ]
        user_profile.professional_data.resume_skills = [
            "Product Strategy", "Team Leadership", "P&L Management"
        ]
        user_profile.skills = [
            Mock(name="Strategic Planning"),
            Mock(name="Executive Leadership"),
            Mock(name="Product Management")
        ]
        
        field, confidence = determine_enhanced_user_career_field(user_profile)
        
        # Should be detected as executive leadership, not just technology
        assert field in ['executive_leadership', 'business_finance']  # Both are valid for exec roles
        assert confidence > 0.5


class TestEnhancedCategorizationEngine:
    """Test the enhanced categorization engine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.thresholds = CategorizationThresholds(
            safe_zone_min=0.8,
            stretch_zone_min=0.6,
            adventure_zone_min=0.4
        )
        self.engine = EnhancedCategorizationEngine(self.thresholds)
    
    def test_inappropriate_recommendation_prevention(self):
        """Test that inappropriate recommendations are prevented."""
        # Mock SVP of Product user profile
        user_profile = Mock(spec=UserProfile)
        user_profile.professional_data = Mock()
        user_profile.professional_data.experience = [
            Mock(title="Senior Vice President of Product Management", duration_years=3)
        ]
        user_profile.professional_data.resume_skills = ["Product Strategy", "Leadership"]
        user_profile.skills = [
            Mock(name="Product Management"),
            Mock(name="Strategic Planning")
        ]
        
        # Mock Police Chief career
        police_career = Mock(spec=Career)
        police_career.career_id = "police_chief_001"
        police_career.career_field = None
        police_career.title = "Police Chief"
        police_career.description = "Lead law enforcement operations"
        police_career.required_skills = [
            Mock(name="Law Enforcement", is_mandatory=True),
            Mock(name="Public Safety", is_mandatory=True)
        ]
        
        # Mock a low score for this inappropriate match
        score = Mock(spec=RecommendationScore)
        score.career_id = "police_chief_001"
        score.total_score = 0.3  # Low score
        score.skill_match_score = 0.1  # Very low skill match
        score.breakdown = {
            "skill_details": {"matched_skills": [], "missing_mandatory": ["Law Enforcement", "Public Safety"]},
            "interest_details": {"matched_interests": []},
            "salary_details": {"compatibility": "unknown"},
            "experience_details": {"experience_level": "executive"}
        }
        
        # Test categorization
        recommendations = self.engine.categorize_recommendations(
            user_profile, [police_career], [score]
        )
        
        assert len(recommendations) == 1
        recommendation = recommendations[0]
        
        # Should be Adventure Zone with low confidence due to field mismatch
        assert recommendation.category == RecommendationCategory.ADVENTURE_ZONE
        assert recommendation.confidence < 0.5  # Low confidence for inappropriate match
        
        # Reasons should indicate this is a field change
        reasons_text = " ".join(recommendation.reasons).lower()
        assert "field" in reasons_text or "explore" in reasons_text
    
    def test_appropriate_executive_recommendation(self):
        """Test that appropriate executive recommendations work well."""
        # Mock SVP of Product user profile
        user_profile = Mock(spec=UserProfile)
        user_profile.professional_data = Mock()
        user_profile.professional_data.experience = [
            Mock(title="Senior Vice President of Product Management", duration_years=3)
        ]
        user_profile.professional_data.resume_skills = ["Product Strategy", "Leadership"]
        user_profile.skills = [
            Mock(name="Product Management"),
            Mock(name="Strategic Planning")
        ]
        
        # Mock CEO career (appropriate executive transition)
        ceo_career = Mock(spec=Career)
        ceo_career.career_id = "ceo_001"
        ceo_career.career_field = None
        ceo_career.title = "Chief Executive Officer"
        ceo_career.description = "Lead entire organization and set strategic vision"
        ceo_career.required_skills = [
            Mock(name="Strategic Planning", is_mandatory=True),
            Mock(name="Leadership", is_mandatory=True)
        ]
        
        # Mock a higher score for this appropriate match
        score = Mock(spec=RecommendationScore)
        score.career_id = "ceo_001"
        score.total_score = 0.85  # High score
        score.skill_match_score = 0.8  # Good skill match
        score.breakdown = {
            "skill_details": {"matched_skills": [{"name": "Strategic Planning"}, {"name": "Leadership"}], "missing_mandatory": []},
            "interest_details": {"matched_interests": []},
            "salary_details": {"compatibility": "compatible"},
            "experience_details": {"experience_level": "executive"}
        }
        
        # Test categorization
        recommendations = self.engine.categorize_recommendations(
            user_profile, [ceo_career], [score]
        )
        
        assert len(recommendations) == 1
        recommendation = recommendations[0]
        
        # Should be Safe or Stretch Zone with high confidence
        assert recommendation.category in [RecommendationCategory.SAFE_ZONE, RecommendationCategory.STRETCH_ZONE]
        assert recommendation.confidence > 0.7  # High confidence for appropriate match
        
        # Reasons should indicate field alignment
        reasons_text = " ".join(recommendation.reasons).lower()
        assert "expertise" in reasons_text or "alignment" in reasons_text or "match" in reasons_text


class TestFieldTransitionLogic:
    """Test field transition logic."""
    
    def test_related_field_transitions(self):
        """Test that related field transitions are handled appropriately."""
        # Technology to Business Finance should be considered related
        tech_fields = ENHANCED_CAREER_FIELD_CATEGORIES['technology']
        business_fields = ENHANCED_CAREER_FIELD_CATEGORIES['business_finance']
        
        assert 'business_finance' in tech_fields.related_fields
        assert 'technology' in business_fields.related_fields
    
    def test_unrelated_field_detection(self):
        """Test that unrelated fields are properly identified."""
        # Technology to Healthcare should not be directly related
        tech_fields = ENHANCED_CAREER_FIELD_CATEGORIES['technology']
        
        assert 'healthcare' not in tech_fields.related_fields


if __name__ == "__main__":
    pytest.main([__file__])