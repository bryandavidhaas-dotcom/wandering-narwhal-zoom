"""
Unit tests for the categorization logic in the recommendation engine.

Tests the CategorizationEngine class and its methods for categorizing
career recommendations into Safe Zone, Stretch Zone, and Adventure Zone.
"""

import unittest
from unittest.mock import Mock

# Import the modules we're testing
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from recommendation_engine.categorization import CategorizationEngine
from recommendation_engine.models import (
    Career, RecommendationScore, CareerRecommendation, RecommendationCategory,
    UserProfile, UserSkill, RequiredSkill, SalaryRange, SkillLevel, Demand
)
from recommendation_engine.config import CategorizationThresholds


class TestCategorizationEngine(unittest.TestCase):
    """Test cases for the CategorizationEngine class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create test thresholds
        self.thresholds = CategorizationThresholds(
            safe_zone_min=0.8,
            stretch_zone_min=0.6,
            adventure_zone_min=0.3
        )
        
        # Create categorization engine
        self.categorization_engine = CategorizationEngine(self.thresholds)
        
        # Create test user profile
        self.user_profile = UserProfile(
            user_id="test_user",
            personal_info=Mock(),
            assessment_results=Mock(),
            professional_data=Mock(),
            skills=[
                UserSkill(
                    skill_id="skill_1",
                    name="Python",
                    level=SkillLevel.ADVANCED,
                    years_experience=3.0,
                    is_certified=False,
                    last_used=None
                ),
                UserSkill(
                    skill_id="skill_2",
                    name="Data Analysis",
                    level=SkillLevel.INTERMEDIATE,
                    years_experience=2.0,
                    is_certified=False,
                    last_used=None
                )
            ],
            user_interests=[]
        )
        
        # Create test careers
        self.careers = [
            Career(
                career_id="career_1",
                title="Data Scientist",
                description="Analyzes data using Python and machine learning",
                required_skills=[
                    RequiredSkill(skill_id="skill_1", name="Python", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                    RequiredSkill(skill_id="skill_2", name="Data Analysis", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.8)
                ],
                salary_range=SalaryRange(min=90000, max=140000, currency="USD"),
                demand=Demand.HIGH,
                related_careers=[],
                growth_potential="Excellent",
                work_environment="Tech companies",
                education_requirements="Bachelor's degree"
            ),
            Career(
                career_id="career_2",
                title="Machine Learning Engineer",
                description="Develops ML models and systems",
                required_skills=[
                    RequiredSkill(skill_id="skill_1", name="Python", proficiency=SkillLevel.EXPERT, is_mandatory=True, weight=1.0),
                    RequiredSkill(skill_id="skill_3", name="Machine Learning", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                    RequiredSkill(skill_id="skill_4", name="Deep Learning", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.8)
                ],
                salary_range=SalaryRange(min=120000, max=180000, currency="USD"),
                demand=Demand.VERY_HIGH,
                related_careers=[],
                growth_potential="Excellent",
                work_environment="Tech companies",
                education_requirements="Master's degree preferred"
            ),
            Career(
                career_id="career_3",
                title="Product Manager",
                description="Manages product development and strategy",
                required_skills=[
                    RequiredSkill(skill_id="skill_5", name="Product Management", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                    RequiredSkill(skill_id="skill_6", name="Leadership", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=0.9),
                    RequiredSkill(skill_id="skill_7", name="Strategy", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.7)
                ],
                salary_range=SalaryRange(min=110000, max=160000, currency="USD"),
                demand=Demand.MEDIUM,
                related_careers=[],
                growth_potential="Good",
                work_environment="Various industries",
                education_requirements="Bachelor's degree"
            )
        ]
        
        # Create test scores
        self.scores = [
            RecommendationScore(
                career_id="career_1",
                total_score=0.85,  # Safe zone
                skill_match_score=0.9,
                interest_match_score=0.8,
                salary_compatibility_score=0.85,
                experience_match_score=0.8,
                breakdown={
                    "skill_details": {
                        "matched_skills": [
                            {"name": "Python", "user_level": "advanced", "required_level": "advanced", "is_certified": False},
                            {"name": "Data Analysis", "user_level": "intermediate", "required_level": "intermediate", "is_certified": False}
                        ],
                        "missing_mandatory": [],
                        "missing_preferred": []
                    },
                    "interest_details": {
                        "matched_interests": [{"interest": "Technology", "level": "very_high"}],
                        "user_interests": ["Technology", "Data Analysis"],
                        "additional_interests": ["AI Ethics"]
                    },
                    "salary_details": {
                        "user_expectations": {"min": 80000, "max": 120000, "currency": "USD"},
                        "career_range": {"min": 90000, "max": 140000, "currency": "USD"},
                        "compatibility": "compatible"
                    },
                    "experience_details": {
                        "total_years": 3.5,
                        "experience_level": "junior",
                        "relevant_experience": []
                    }
                }
            ),
            RecommendationScore(
                career_id="career_2",
                total_score=0.65,  # Stretch zone
                skill_match_score=0.6,
                interest_match_score=0.7,
                salary_compatibility_score=0.6,
                experience_match_score=0.7,
                breakdown={
                    "skill_details": {
                        "matched_skills": [
                            {"name": "Python", "user_level": "advanced", "required_level": "expert", "is_certified": False}
                        ],
                        "missing_mandatory": ["Machine Learning", "Deep Learning"],
                        "missing_preferred": []
                    },
                    "interest_details": {
                        "matched_interests": [{"interest": "Technology", "level": "very_high"}],
                        "user_interests": ["Technology", "Machine Learning"],
                        "additional_interests": []
                    },
                    "salary_details": {
                        "user_expectations": {"min": 80000, "max": 120000, "currency": "USD"},
                        "career_range": {"min": 120000, "max": 180000, "currency": "USD"},
                        "compatibility": "higher_than_expected"
                    },
                    "experience_details": {
                        "total_years": 3.5,
                        "experience_level": "junior",
                        "relevant_experience": []
                    }
                }
            ),
            RecommendationScore(
                career_id="career_3",
                total_score=0.4,  # Adventure zone
                skill_match_score=0.2,
                interest_match_score=0.5,
                salary_compatibility_score=0.7,
                experience_match_score=0.3,
                breakdown={
                    "skill_details": {
                        "matched_skills": [],
                        "missing_mandatory": ["Product Management", "Leadership", "Strategy"],
                        "missing_preferred": []
                    },
                    "interest_details": {
                        "matched_interests": [],
                        "user_interests": ["Technology"],
                        "additional_interests": []
                    },
                    "salary_details": {
                        "user_expectations": {"min": 80000, "max": 120000, "currency": "USD"},
                        "career_range": {"min": 110000, "max": 160000, "currency": "USD"},
                        "compatibility": "higher_than_expected"
                    },
                    "experience_details": {
                        "total_years": 3.5,
                        "experience_level": "junior",
                        "relevant_experience": []
                    }
                }
            )
        ]
    
    def test_categorize_recommendations_complete(self):
        """Test complete recommendation categorization."""
        recommendations = self.categorization_engine.categorize_recommendations(
            self.user_profile, self.careers, self.scores
        )
        
        # Should return list of CareerRecommendation objects
        self.assertIsInstance(recommendations, list)
        self.assertEqual(len(recommendations), 3)
        
        for rec in recommendations:
            self.assertIsInstance(rec, CareerRecommendation)
            self.assertIsInstance(rec.category, RecommendationCategory)
            self.assertIsInstance(rec.reasons, list)
            self.assertIsInstance(rec.confidence, float)
            self.assertGreaterEqual(rec.confidence, 0.0)
            self.assertLessEqual(rec.confidence, 1.0)
    
    def test_determine_category_safe_zone(self):
        """Test categorization into Safe Zone."""
        # High total score and high skill score
        category = self.categorization_engine._determine_category(
            self.scores[0], self.user_profile, self.careers[0]
        )
        
        self.assertEqual(category, RecommendationCategory.SAFE_ZONE)
    
    def test_determine_category_stretch_zone_high_score_low_skills(self):
        """Test categorization into Stretch Zone due to high score but lower skill match."""
        # Create score with high total but lower skill score
        stretch_score = RecommendationScore(
            career_id="career_stretch",
            total_score=0.82,  # Above safe zone threshold
            skill_match_score=0.7,  # Below 0.8 skill threshold
            interest_match_score=0.9,
            salary_compatibility_score=0.8,
            experience_match_score=0.8,
            breakdown={}
        )
        
        category = self.categorization_engine._determine_category(
            stretch_score, self.user_profile, self.careers[0]
        )
        
        self.assertEqual(category, RecommendationCategory.STRETCH_ZONE)
    
    def test_determine_category_stretch_zone_medium_score(self):
        """Test categorization into Stretch Zone with medium score."""
        category = self.categorization_engine._determine_category(
            self.scores[1], self.user_profile, self.careers[1]
        )
        
        self.assertEqual(category, RecommendationCategory.STRETCH_ZONE)
    
    def test_determine_category_adventure_zone(self):
        """Test categorization into Adventure Zone."""
        category = self.categorization_engine._determine_category(
            self.scores[2], self.user_profile, self.careers[2]
        )
        
        self.assertEqual(category, RecommendationCategory.ADVENTURE_ZONE)
    
    def test_determine_category_adventure_zone_low_score(self):
        """Test categorization into Adventure Zone with very low score."""
        # Create score below adventure zone threshold
        low_score = RecommendationScore(
            career_id="career_low",
            total_score=0.2,  # Below adventure zone threshold
            skill_match_score=0.1,
            interest_match_score=0.3,
            salary_compatibility_score=0.2,
            experience_match_score=0.2,
            breakdown={}
        )
        
        category = self.categorization_engine._determine_category(
            low_score, self.user_profile, self.careers[0]
        )
        
        self.assertEqual(category, RecommendationCategory.ADVENTURE_ZONE)
    
    def test_generate_reasons_safe_zone(self):
        """Test reason generation for Safe Zone recommendations."""
        reasons = self.categorization_engine._generate_reasons(
            self.scores[0], self.user_profile, self.careers[0], RecommendationCategory.SAFE_ZONE
        )
        
        self.assertIsInstance(reasons, list)
        self.assertGreater(len(reasons), 0)
        self.assertLessEqual(len(reasons), 5)  # Should limit to 5 reasons
        
        # Should include skill-based reasons
        skill_reasons = [r for r in reasons if "skills" in r.lower()]
        self.assertGreater(len(skill_reasons), 0)
        
        # Should include safe zone specific reason
        safe_zone_reasons = [r for r in reasons if "low risk" in r.lower()]
        self.assertGreater(len(safe_zone_reasons), 0)
    
    def test_generate_reasons_stretch_zone(self):
        """Test reason generation for Stretch Zone recommendations."""
        reasons = self.categorization_engine._generate_reasons(
            self.scores[1], self.user_profile, self.careers[1], RecommendationCategory.STRETCH_ZONE
        )
        
        self.assertIsInstance(reasons, list)
        self.assertGreater(len(reasons), 0)
        
        # Should include stretch zone specific reason
        stretch_reasons = [r for r in reasons if "additional skill development" in r.lower()]
        self.assertGreater(len(stretch_reasons), 0)
    
    def test_generate_reasons_adventure_zone(self):
        """Test reason generation for Adventure Zone recommendations."""
        reasons = self.categorization_engine._generate_reasons(
            self.scores[2], self.user_profile, self.careers[2], RecommendationCategory.ADVENTURE_ZONE
        )
        
        self.assertIsInstance(reasons, list)
        self.assertGreater(len(reasons), 0)
        
        # Should include adventure zone specific reason
        adventure_reasons = [r for r in reasons if "exciting opportunity" in r.lower() or "new career direction" in r.lower()]
        self.assertGreater(len(adventure_reasons), 0)
    
    def test_generate_reasons_skill_based(self):
        """Test skill-based reason generation."""
        # Test high skill match
        high_skill_score = RecommendationScore(
            career_id="high_skill",
            total_score=0.8,
            skill_match_score=0.9,  # High skill match
            interest_match_score=0.7,
            salary_compatibility_score=0.8,
            experience_match_score=0.8,
            breakdown={
                "skill_details": {
                    "matched_skills": [
                        {"name": "Python", "user_level": "advanced", "required_level": "advanced", "is_certified": False},
                        {"name": "Data Analysis", "user_level": "advanced", "required_level": "intermediate", "is_certified": False}
                    ],
                    "missing_mandatory": [],
                    "missing_preferred": []
                }
            }
        )
        
        reasons = self.categorization_engine._generate_reasons(
            high_skill_score, self.user_profile, self.careers[0], RecommendationCategory.SAFE_ZONE
        )
        
        # Should mention strong skill match
        skill_match_reasons = [r for r in reasons if "strong match" in r.lower() and "skills" in r.lower()]
        self.assertGreater(len(skill_match_reasons), 0)
    
    def test_generate_reasons_missing_skills(self):
        """Test reason generation for missing skills."""
        reasons = self.categorization_engine._generate_reasons(
            self.scores[1], self.user_profile, self.careers[1], RecommendationCategory.STRETCH_ZONE
        )
        
        # Should mention skills to develop
        development_reasons = [r for r in reasons if "developing" in r.lower() or "learn" in r.lower()]
        self.assertGreater(len(development_reasons), 0)
    
    def test_generate_reasons_salary_compatibility(self):
        """Test salary-based reason generation."""
        # Test compatible salary
        compatible_reasons = self.categorization_engine._generate_reasons(
            self.scores[0], self.user_profile, self.careers[0], RecommendationCategory.SAFE_ZONE
        )
        
        salary_reasons = [r for r in compatible_reasons if "salary" in r.lower() and "matches" in r.lower()]
        self.assertGreater(len(salary_reasons), 0)
        
        # Test higher than expected salary
        higher_reasons = self.categorization_engine._generate_reasons(
            self.scores[1], self.user_profile, self.careers[1], RecommendationCategory.STRETCH_ZONE
        )
        
        higher_salary_reasons = [r for r in higher_reasons if "higher compensation" in r.lower()]
        self.assertGreater(len(higher_salary_reasons), 0)
    
    def test_generate_reasons_market_demand(self):
        """Test market demand reason generation."""
        # Create career with high demand
        high_demand_career = Career(
            career_id="high_demand",
            title="High Demand Role",
            description="Role with high market demand",
            required_skills=[],
            salary_range=SalaryRange(min=80000, max=120000, currency="USD"),
            demand=Demand.HIGH,
            related_careers=[],
            growth_potential="Excellent",
            work_environment="Various",
            education_requirements="Bachelor's"
        )
        
        reasons = self.categorization_engine._generate_reasons(
            self.scores[0], self.user_profile, high_demand_career, RecommendationCategory.SAFE_ZONE
        )
        
        # Should mention high market demand
        demand_reasons = [r for r in reasons if "high market demand" in r.lower() or "high demand" in r.lower()]
        self.assertGreater(len(demand_reasons), 0)
    
    def test_calculate_confidence_safe_zone(self):
        """Test confidence calculation for Safe Zone."""
        confidence = self.categorization_engine._calculate_confidence(
            self.scores[0], RecommendationCategory.SAFE_ZONE
        )
        
        # Should boost confidence for safe zone
        self.assertGreater(confidence, self.scores[0].total_score)
        self.assertLessEqual(confidence, 1.0)
    
    def test_calculate_confidence_stretch_zone(self):
        """Test confidence calculation for Stretch Zone."""
        confidence = self.categorization_engine._calculate_confidence(
            self.scores[1], RecommendationCategory.STRETCH_ZONE
        )
        
        # Should maintain base confidence for stretch zone
        self.assertEqual(confidence, self.scores[1].total_score)
    
    def test_calculate_confidence_adventure_zone(self):
        """Test confidence calculation for Adventure Zone."""
        confidence = self.categorization_engine._calculate_confidence(
            self.scores[2], RecommendationCategory.ADVENTURE_ZONE
        )
        
        # Should reduce confidence for adventure zone but maintain minimum
        self.assertLess(confidence, self.scores[2].total_score)
        self.assertGreaterEqual(confidence, 0.3)
    
    def test_count_missing_mandatory_skills(self):
        """Test counting missing mandatory skills."""
        # User has Python and Data Analysis
        # Career 1 requires Python (mandatory) and Data Analysis (mandatory) - should be 0 missing
        missing_count_1 = self.categorization_engine._count_missing_mandatory_skills(
            self.user_profile, self.careers[0]
        )
        self.assertEqual(missing_count_1, 0)
        
        # Career 2 requires Python, Machine Learning, Deep Learning (all mandatory) - should be 2 missing
        missing_count_2 = self.categorization_engine._count_missing_mandatory_skills(
            self.user_profile, self.careers[1]
        )
        self.assertEqual(missing_count_2, 2)
        
        # Career 3 requires Product Management, Leadership, Strategy (all mandatory) - should be 3 missing
        missing_count_3 = self.categorization_engine._count_missing_mandatory_skills(
            self.user_profile, self.careers[2]
        )
        self.assertEqual(missing_count_3, 3)
    
    def test_get_category_distribution(self):
        """Test category distribution calculation."""
        recommendations = self.categorization_engine.categorize_recommendations(
            self.user_profile, self.careers, self.scores
        )
        
        distribution = self.categorization_engine.get_category_distribution(recommendations)
        
        # Should return dictionary with expected keys
        expected_keys = ["safe_zone", "stretch_zone", "adventure_zone"]
        for key in expected_keys:
            self.assertIn(key, distribution)
            self.assertIsInstance(distribution[key], int)
            self.assertGreaterEqual(distribution[key], 0)
        
        # Total should equal number of recommendations
        total = sum(distribution.values())
        self.assertEqual(total, len(recommendations))
    
    def test_filter_by_category(self):
        """Test filtering recommendations by category."""
        recommendations = self.categorization_engine.categorize_recommendations(
            self.user_profile, self.careers, self.scores
        )
        
        # Filter by each category
        safe_zone_recs = self.categorization_engine.filter_by_category(
            recommendations, RecommendationCategory.SAFE_ZONE
        )
        stretch_zone_recs = self.categorization_engine.filter_by_category(
            recommendations, RecommendationCategory.STRETCH_ZONE
        )
        adventure_zone_recs = self.categorization_engine.filter_by_category(
            recommendations, RecommendationCategory.ADVENTURE_ZONE
        )
        
        # All filtered recommendations should have the correct category
        for rec in safe_zone_recs:
            self.assertEqual(rec.category, RecommendationCategory.SAFE_ZONE)
        
        for rec in stretch_zone_recs:
            self.assertEqual(rec.category, RecommendationCategory.STRETCH_ZONE)
        
        for rec in adventure_zone_recs:
            self.assertEqual(rec.category, RecommendationCategory.ADVENTURE_ZONE)
        
        # Total should equal original recommendations
        total_filtered = len(safe_zone_recs) + len(stretch_zone_recs) + len(adventure_zone_recs)
        self.assertEqual(total_filtered, len(recommendations))
    
    def test_get_top_recommendations_per_category(self):
        """Test getting top recommendations per category."""
        recommendations = self.categorization_engine.categorize_recommendations(
            self.user_profile, self.careers, self.scores
        )
        
        top_recs = self.categorization_engine.get_top_recommendations_per_category(
            recommendations, limit_per_category=2
        )
        
        # Should return dictionary with expected keys
        expected_keys = ["safe_zone", "stretch_zone", "adventure_zone"]
        for key in expected_keys:
            self.assertIn(key, top_recs)
            self.assertIsInstance(top_recs[key], list)
            self.assertLessEqual(len(top_recs[key]), 2)  # Should respect limit
        
        # Each category should be sorted by score (descending)
        for category_recs in top_recs.values():
            for i in range(len(category_recs) - 1):
                self.assertGreaterEqual(
                    category_recs[i].score.total_score,
                    category_recs[i + 1].score.total_score
                )


class TestCategorizationEngineEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions for CategorizationEngine."""
    
    def setUp(self):
        """Set up test fixtures for edge cases."""
        self.thresholds = CategorizationThresholds(
            safe_zone_min=0.8,
            stretch_zone_min=0.6,
            adventure_zone_min=0.3
        )
        self.categorization_engine = CategorizationEngine(self.thresholds)
    
    def test_empty_recommendations(self):
        """Test handling empty recommendations list."""
        user_profile = Mock()
        empty_careers = []
        empty_scores = []
        
        recommendations = self.categorization_engine.categorize_recommendations(
            user_profile, empty_careers, empty_scores
        )
        
        self.assertEqual(len(recommendations), 0)
    
    def test_mismatched_careers_and_scores(self):
        """Test handling mismatched careers and scores."""
        user_profile = Mock()
        careers = [Mock()]
        careers[0].career_id = "career_1"
        
        # Score for different career ID
        scores = [Mock()]
        scores[0].career_id = "career_2"  # Different ID
        
        recommendations = self.categorization_engine.categorize_recommendations(
            user_profile, careers, scores
        )
        
        # Should handle gracefully and return empty list
        self.assertEqual(len(recommendations), 0)
    
    def test_boundary_score_values(self):
        """Test categorization with boundary score values."""
        user_profile = Mock()
        user_profile.skills = []
        
        career = Mock()
        career.career_id = "boundary_career"
        career.required_skills = []
        career.demand = Mock()
        career.demand.value = "medium"
        
        # Test exact threshold values
        boundary_scores = [
            (0.8, RecommendationCategory.SAFE_ZONE),    # Exact safe zone threshold
            (0.6, RecommendationCategory.STRETCH_ZONE), # Exact stretch zone threshold
            (0.3, RecommendationCategory.ADVENTURE_ZONE) # Exact adventure zone threshold
        ]
        
        for score_value, expected_category in boundary_scores:
            score = Mock()
            score.total_score = score_value
            score.skill_match_score = 0.5
            score.breakdown = {"skill_details": {}, "interest_details": {}, "salary_details": {}, "experience_details": {}}
            
            category = self.categorization_engine._determine_category(score, user_profile, career)
            self.assertEqual(category, expected_category)


if __name__ == '__main__':
    unittest.main()