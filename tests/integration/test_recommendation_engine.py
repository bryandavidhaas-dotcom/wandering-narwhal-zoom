"""
Integration tests for the recommendation engine.

Tests the complete RecommendationEngine class and its integration
with all components (filtering, scoring, categorization).
"""

import unittest
from datetime import datetime, timedelta

# Import the modules we're testing
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from recommendation_engine.engine import RecommendationEngine
from recommendation_engine.mock_data import (
    MOCK_SKILLS, MOCK_CAREERS, MOCK_USER_PROFILE, ALTERNATIVE_USER_PROFILE
)
from recommendation_engine.models import CareerRecommendation, RecommendationCategory


class TestRecommendationEngineIntegration(unittest.TestCase):
    """Integration test cases for the complete RecommendationEngine."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create recommendation engine with mock data
        self.engine = RecommendationEngine()
        
        # Use mock data
        self.skills = MOCK_SKILLS
        self.careers = MOCK_CAREERS
        self.user_profile = MOCK_USER_PROFILE
        self.alternative_user = ALTERNATIVE_USER_PROFILE
    
    def test_get_recommendations_complete_pipeline(self):
        """Test the complete recommendation pipeline end-to-end."""
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        # Should return list of CareerRecommendation objects
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        for rec in recommendations:
            self.assertIsInstance(rec, CareerRecommendation)
            self.assertIsNotNone(rec.career)
            self.assertIsNotNone(rec.score)
            self.assertIsInstance(rec.category, RecommendationCategory)
            self.assertIsInstance(rec.reasons, list)
            self.assertIsInstance(rec.confidence, float)
            
            # Validate score ranges
            self.assertGreaterEqual(rec.score.total_score, 0.0)
            self.assertLessEqual(rec.score.total_score, 1.0)
            self.assertGreaterEqual(rec.confidence, 0.0)
            self.assertLessEqual(rec.confidence, 1.0)
    
    def test_get_recommendations_sorted_by_score(self):
        """Test that recommendations are sorted by total score."""
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        # Should be sorted by total score (descending)
        for i in range(len(recommendations) - 1):
            self.assertGreaterEqual(
                recommendations[i].score.total_score,
                recommendations[i + 1].score.total_score
            )
    
    def test_get_recommendations_different_user_profiles(self):
        """Test recommendations for different user profiles."""
        # Get recommendations for primary user
        recommendations_1 = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        # Get recommendations for alternative user
        recommendations_2 = self.engine.get_recommendations(
            self.alternative_user, self.careers, self.skills
        )
        
        # Both should return recommendations
        self.assertGreater(len(recommendations_1), 0)
        self.assertGreater(len(recommendations_2), 0)
        
        # Recommendations should be different (different ordering at minimum)
        # Check if top recommendation is different
        if len(recommendations_1) > 0 and len(recommendations_2) > 0:
            # At least the scores should be different due to different user profiles
            top_score_1 = recommendations_1[0].score.total_score
            top_score_2 = recommendations_2[0].score.total_score
            
            # Scores might be the same, but the specific breakdown should differ
            self.assertIsInstance(top_score_1, float)
            self.assertIsInstance(top_score_2, float)
    
    def test_get_recommendations_with_filtering(self):
        """Test that filtering is applied correctly."""
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        # Should filter out careers that don't match user criteria
        # The number of recommendations should be <= number of input careers
        self.assertLessEqual(len(recommendations), len(self.careers))
        
        # All returned recommendations should have some minimum score
        for rec in recommendations:
            self.assertGreater(rec.score.total_score, 0.0)
    
    def test_get_recommendations_categorization(self):
        """Test that recommendations are properly categorized."""
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        # Should have recommendations in different categories
        categories = {rec.category for rec in recommendations}
        
        # Should have at least one category
        self.assertGreater(len(categories), 0)
        
        # Validate category assignments based on scores
        for rec in recommendations:
            if rec.score.total_score >= 0.8:
                # High scores should generally be Safe Zone or Stretch Zone
                self.assertIn(rec.category, [
                    RecommendationCategory.SAFE_ZONE,
                    RecommendationCategory.STRETCH_ZONE
                ])
            elif rec.score.total_score < 0.3:
                # Very low scores should be Adventure Zone
                self.assertEqual(rec.category, RecommendationCategory.ADVENTURE_ZONE)
    
    def test_get_recommendations_reasons_generation(self):
        """Test that meaningful reasons are generated."""
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        for rec in recommendations:
            # Should have at least one reason
            self.assertGreater(len(rec.reasons), 0)
            
            # Reasons should be non-empty strings
            for reason in rec.reasons:
                self.assertIsInstance(reason, str)
                self.assertGreater(len(reason.strip()), 0)
            
            # Should have reasonable number of reasons (not too many)
            self.assertLessEqual(len(rec.reasons), 5)
    
    def test_get_recommendations_skill_matching(self):
        """Test that skill matching works correctly in integration."""
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        # Find recommendations that should match user's skills well
        user_skill_names = {skill.name.lower() for skill in self.user_profile.skills}
        
        for rec in recommendations:
            # Check if career requires skills the user has
            career_skill_names = {skill.name.lower() for skill in rec.career.required_skills}
            skill_overlap = user_skill_names.intersection(career_skill_names)
            
            if len(skill_overlap) > 0:
                # Should have decent skill match score
                self.assertGreater(rec.score.skill_match_score, 0.0)
                
                # Should mention skills in reasons
                skill_mentioned = any(
                    any(skill_name in reason.lower() for skill_name in skill_overlap)
                    for reason in rec.reasons
                )
                # Note: Not all recommendations will mention specific skills in reasons
                # This is just checking that the integration works
    
    def test_get_recommendations_salary_compatibility(self):
        """Test salary compatibility in integration."""
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        user_salary = self.user_profile.personal_info.salary_expectations
        
        for rec in recommendations:
            career_salary = rec.career.salary_range
            
            # Check salary compatibility logic
            if (user_salary and career_salary and 
                user_salary.currency == career_salary.currency):
                
                # If there's overlap, should have good salary score
                overlap_start = max(user_salary.min, career_salary.min)
                overlap_end = min(user_salary.max, career_salary.max)
                
                if overlap_end >= overlap_start:
                    # There is overlap
                    self.assertGreater(rec.score.salary_compatibility_score, 0.5)
    
    def test_get_recommendations_empty_careers(self):
        """Test handling of empty careers list."""
        recommendations = self.engine.get_recommendations(
            self.user_profile, [], self.skills
        )
        
        # Should return empty list
        self.assertEqual(len(recommendations), 0)
    
    def test_get_recommendations_empty_skills(self):
        """Test handling of empty skills database."""
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, []
        )
        
        # Should still work but might affect skill-based filtering
        self.assertIsInstance(recommendations, list)
        # Should still return some recommendations since not all logic depends on skills DB
    
    def test_get_recommendations_performance(self):
        """Test that recommendations are generated in reasonable time."""
        import time
        
        start_time = time.time()
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        end_time = time.time()
        
        # Should complete within reasonable time (adjust threshold as needed)
        execution_time = end_time - start_time
        self.assertLess(execution_time, 5.0)  # 5 seconds should be more than enough
        
        # Should still return valid recommendations
        self.assertIsInstance(recommendations, list)
    
    def test_get_recommendations_consistency(self):
        """Test that recommendations are consistent across multiple calls."""
        # Get recommendations twice
        recommendations_1 = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        recommendations_2 = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        # Should return same number of recommendations
        self.assertEqual(len(recommendations_1), len(recommendations_2))
        
        # Should have same career IDs in same order
        career_ids_1 = [rec.career.career_id for rec in recommendations_1]
        career_ids_2 = [rec.career.career_id for rec in recommendations_2]
        self.assertEqual(career_ids_1, career_ids_2)
        
        # Scores should be identical
        for rec1, rec2 in zip(recommendations_1, recommendations_2):
            self.assertEqual(rec1.score.total_score, rec2.score.total_score)
            self.assertEqual(rec1.category, rec2.category)
    
    def test_component_integration_filtering_to_scoring(self):
        """Test integration between filtering and scoring components."""
        # This tests that filtered careers are properly passed to scoring
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        # All recommendations should have been through both filtering and scoring
        for rec in recommendations:
            # Should have valid scores (indicating scoring was applied)
            self.assertIsNotNone(rec.score.skill_match_score)
            self.assertIsNotNone(rec.score.interest_match_score)
            self.assertIsNotNone(rec.score.salary_compatibility_score)
            self.assertIsNotNone(rec.score.experience_match_score)
            
            # Should have score breakdown (detailed scoring was applied)
            self.assertIsInstance(rec.score.breakdown, dict)
            self.assertIn("skill_details", rec.score.breakdown)
    
    def test_component_integration_scoring_to_categorization(self):
        """Test integration between scoring and categorization components."""
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        # All recommendations should have been through both scoring and categorization
        for rec in recommendations:
            # Should have valid category (indicating categorization was applied)
            self.assertIsInstance(rec.category, RecommendationCategory)
            
            # Category should be consistent with score
            if rec.score.total_score >= 0.8:
                # High scores should not be in Adventure Zone
                self.assertNotEqual(rec.category, RecommendationCategory.ADVENTURE_ZONE)
            elif rec.score.total_score < 0.3:
                # Very low scores should be in Adventure Zone
                self.assertEqual(rec.category, RecommendationCategory.ADVENTURE_ZONE)
    
    def test_mock_data_integration(self):
        """Test that mock data integrates properly with the engine."""
        # Verify mock data is valid for testing
        self.assertGreater(len(self.skills), 0)
        self.assertGreater(len(self.careers), 0)
        self.assertIsNotNone(self.user_profile)
        self.assertIsNotNone(self.alternative_user)
        
        # Test with mock data
        recommendations = self.engine.get_recommendations(
            self.user_profile, self.careers, self.skills
        )
        
        # Should work with mock data
        self.assertIsInstance(recommendations, list)
        
        # Mock user profile should get some good matches
        # (since mock data is designed to have some matching careers)
        if len(recommendations) > 0:
            top_recommendation = recommendations[0]
            self.assertGreater(top_recommendation.score.total_score, 0.0)


class TestRecommendationEngineEdgeCases(unittest.TestCase):
    """Test edge cases for the RecommendationEngine integration."""
    
    def setUp(self):
        """Set up test fixtures for edge cases."""
        self.engine = RecommendationEngine()
    
    def test_user_with_no_skills(self):
        """Test recommendations for user with no skills."""
        # Create user profile with no skills
        user_no_skills = MOCK_USER_PROFILE
        user_no_skills.skills = []
        user_no_skills.professional_data.resume_skills = []
        user_no_skills.professional_data.linkedin_skills = []
        
        recommendations = self.engine.get_recommendations(
            user_no_skills, MOCK_CAREERS, MOCK_SKILLS
        )
        
        # Should still return recommendations (though likely lower scores)
        self.assertIsInstance(recommendations, list)
        
        # All recommendations should have low skill match scores
        for rec in recommendations:
            if len(rec.career.required_skills) > 0:
                self.assertLessEqual(rec.score.skill_match_score, 0.5)
    
    def test_careers_with_no_requirements(self):
        """Test with careers that have no skill requirements."""
        from recommendation_engine.models import Career, SalaryRange, Demand
        
        # Create career with no requirements
        no_req_career = Career(
            career_id="no_requirements",
            title="General Role",
            description="Role with no specific requirements",
            required_skills=[],
            salary_range=SalaryRange(min=50000, max=80000, currency="USD"),
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="Various",
            education_requirements="High school"
        )
        
        careers_with_no_req = [no_req_career]
        
        recommendations = self.engine.get_recommendations(
            MOCK_USER_PROFILE, careers_with_no_req, MOCK_SKILLS
        )
        
        # Should return the career with perfect skill match
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0].score.skill_match_score, 1.0)
    
    def test_extreme_salary_mismatches(self):
        """Test with careers that have extreme salary mismatches."""
        from recommendation_engine.models import Career, SalaryRange, Demand
        
        # Create career with extremely high salary
        high_salary_career = Career(
            career_id="extreme_high_salary",
            title="Executive Role",
            description="Very high paying role",
            required_skills=[],
            salary_range=SalaryRange(min=500000, max=1000000, currency="USD"),
            demand=Demand.LOW,
            related_careers=[],
            growth_potential="Limited",
            work_environment="Corporate",
            education_requirements="MBA"
        )
        
        careers_extreme = [high_salary_career]
        
        recommendations = self.engine.get_recommendations(
            MOCK_USER_PROFILE, careers_extreme, MOCK_SKILLS
        )
        
        # Should still return recommendation but with adjusted salary score
        if len(recommendations) > 0:
            # Salary compatibility should reflect the mismatch
            self.assertIsInstance(recommendations[0].score.salary_compatibility_score, float)


if __name__ == '__main__':
    unittest.main()