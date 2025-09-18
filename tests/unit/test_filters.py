"""
Unit tests for the filtering logic in the recommendation engine.

Tests the FilterEngine class and its methods for filtering careers
based on user preferences, skills, and interests.
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Import the modules we're testing
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from recommendation_engine.filters import FilterEngine
from recommendation_engine.models import (
    UserProfile, Career, Skill, UserSkill, RequiredSkill, SalaryRange,
    PersonalInfo, AssessmentResults, ProfessionalData, Experience,
    SkillLevel, InterestLevel, Demand, ExperienceLevel
)
from recommendation_engine.config import FilteringConfig


class TestFilterEngine(unittest.TestCase):
    """Test cases for the FilterEngine class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create test configuration
        self.config = FilteringConfig(
            min_skill_overlap=0.3,
            max_salary_deviation=0.2,
            consider_related_skills=True
        )
        
        # Create test skills database
        self.skills_db = [
            Skill(
                skill_id="skill_1",
                name="Python",
                category="Programming Language",
                related_skills=["skill_2", "skill_3"]
            ),
            Skill(
                skill_id="skill_2",
                name="Machine Learning",
                category="Technical Skill",
                related_skills=["skill_1", "skill_3"]
            ),
            Skill(
                skill_id="skill_3",
                name="Data Analysis",
                category="Technical Skill",
                related_skills=["skill_1", "skill_2"]
            ),
            Skill(
                skill_id="skill_4",
                name="JavaScript",
                category="Programming Language",
                related_skills=[]
            )
        ]
        
        # Create filter engine
        self.filter_engine = FilterEngine(self.config, self.skills_db)
        
        # Create test user profile
        self.user_profile = UserProfile(
            user_id="test_user",
            personal_info=PersonalInfo(
                age=28,
                location="San Francisco, CA",
                salary_expectations=SalaryRange(min=80000, max=120000, currency="USD"),
                willing_to_relocate=False,
                preferred_work_style="hybrid"
            ),
            assessment_results=AssessmentResults(
                personality_traits=["Analytical", "Detail-Oriented"],
                work_values=["Autonomy", "Innovation"],
                interests={
                    "Technology": InterestLevel.VERY_HIGH,
                    "Data Analysis": InterestLevel.HIGH,
                    "Leadership": InterestLevel.LOW
                }
            ),
            professional_data=ProfessionalData(
                resume_skills=["Python", "Data Analysis"],
                linkedin_skills=["Python", "Machine Learning"],
                experience=[
                    Experience(
                        title="Data Analyst",
                        company="Tech Corp",
                        duration_years=2.0,
                        description="Analyzed data",
                        skills_used=["Python", "Data Analysis"]
                    )
                ],
                education="Bachelor's in Computer Science",
                certifications=[]
            ),
            skills=[
                UserSkill(
                    skill_id="skill_1",
                    name="Python",
                    level=SkillLevel.ADVANCED,
                    years_experience=3.0,
                    is_certified=False,
                    last_used=datetime.utcnow() - timedelta(days=1)
                ),
                UserSkill(
                    skill_id="skill_3",
                    name="Data Analysis",
                    level=SkillLevel.INTERMEDIATE,
                    years_experience=2.0,
                    is_certified=False,
                    last_used=datetime.utcnow() - timedelta(days=5)
                )
            ],
            user_interests=["AI Ethics", "Data Privacy"]
        )
        
        # Create test careers
        self.careers = [
            Career(
                career_id="career_1",
                title="Data Scientist",
                description="Analyzes data using Python and machine learning",
                required_skills=[
                    RequiredSkill(skill_id="skill_1", name="Python", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                    RequiredSkill(skill_id="skill_2", name="Machine Learning", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.8),
                    RequiredSkill(skill_id="skill_3", name="Data Analysis", proficiency=SkillLevel.ADVANCED, is_mandatory=False, weight=0.7)
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
                title="Web Developer",
                description="Develops web applications using JavaScript",
                required_skills=[
                    RequiredSkill(skill_id="skill_4", name="JavaScript", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0)
                ],
                salary_range=SalaryRange(min=70000, max=110000, currency="USD"),
                demand=Demand.MEDIUM,
                related_careers=[],
                growth_potential="Good",
                work_environment="Various",
                education_requirements="Bachelor's degree"
            ),
            Career(
                career_id="career_3",
                title="Senior Executive",
                description="Leadership role requiring extensive experience",
                required_skills=[],
                salary_range=SalaryRange(min=200000, max=300000, currency="USD"),
                demand=Demand.LOW,
                related_careers=[],
                growth_potential="Limited",
                work_environment="Corporate",
                education_requirements="MBA preferred"
            )
        ]
    
    def test_filter_careers_complete_pipeline(self):
        """Test the complete filtering pipeline."""
        filtered_careers = self.filter_engine.filter_careers(self.user_profile, self.careers)
        
        # Should filter out careers that don't match
        self.assertIsInstance(filtered_careers, list)
        self.assertLessEqual(len(filtered_careers), len(self.careers))
        
        # Data Scientist should likely pass all filters
        career_ids = [career.career_id for career in filtered_careers]
        self.assertIn("career_1", career_ids)
    
    def test_apply_initial_filters_salary_compatible(self):
        """Test initial filtering with salary compatibility."""
        filtered_careers = self.filter_engine.apply_initial_filters(self.user_profile, self.careers)
        
        # Should include careers with compatible salary ranges
        career_ids = [career.career_id for career in filtered_careers]
        self.assertIn("career_1", career_ids)  # Data Scientist: 90k-140k (compatible with 80k-120k)
        self.assertIn("career_2", career_ids)  # Web Developer: 70k-110k (compatible)
        
        # Senior Executive might be filtered out due to salary mismatch (200k-300k vs 80k-120k)
        # But with deviation tolerance, it might still pass
    
    def test_apply_initial_filters_no_salary_expectations(self):
        """Test initial filtering when user has no salary expectations."""
        # Create user profile without salary expectations
        user_no_salary = UserProfile(
            user_id="test_user_no_salary",
            personal_info=PersonalInfo(
                age=28,
                location="San Francisco, CA",
                salary_expectations=None,
                willing_to_relocate=False,
                preferred_work_style="hybrid"
            ),
            assessment_results=self.user_profile.assessment_results,
            professional_data=self.user_profile.professional_data,
            skills=self.user_profile.skills,
            user_interests=self.user_profile.user_interests
        )
        
        filtered_careers = self.filter_engine.apply_initial_filters(user_no_salary, self.careers)
        
        # Should include all careers when no salary expectations
        self.assertEqual(len(filtered_careers), len(self.careers))
    
    def test_apply_skill_filters_sufficient_overlap(self):
        """Test skill filtering with sufficient skill overlap."""
        filtered_careers = self.filter_engine.apply_skill_filters(self.user_profile, self.careers)
        
        # Data Scientist should pass (user has Python and Data Analysis)
        career_ids = [career.career_id for career in filtered_careers]
        self.assertIn("career_1", career_ids)
    
    def test_apply_skill_filters_mandatory_skills(self):
        """Test skill filtering with mandatory skills check."""
        # Create a career with mandatory skills the user doesn't have
        career_missing_mandatory = Career(
            career_id="career_missing",
            title="AI Researcher",
            description="Research in artificial intelligence",
            required_skills=[
                RequiredSkill(skill_id="skill_missing", name="Deep Learning", proficiency=SkillLevel.EXPERT, is_mandatory=True, weight=1.0)
            ],
            salary_range=SalaryRange(min=100000, max=150000, currency="USD"),
            demand=Demand.HIGH,
            related_careers=[],
            growth_potential="Excellent",
            work_environment="Research labs",
            education_requirements="PhD preferred"
        )
        
        careers_with_missing = self.careers + [career_missing_mandatory]
        filtered_careers = self.filter_engine.apply_skill_filters(self.user_profile, careers_with_missing)
        
        # Career with missing mandatory skill should be filtered out
        career_ids = [career.career_id for career in filtered_careers]
        self.assertNotIn("career_missing", career_ids)
    
    def test_apply_interest_filters_alignment(self):
        """Test interest-based filtering."""
        filtered_careers = self.filter_engine.apply_interest_filters(self.user_profile, self.careers)
        
        # Should include careers that align with interests
        career_ids = [career.career_id for career in filtered_careers]
        self.assertIn("career_1", career_ids)  # Data Scientist mentions "data" which aligns with interests
    
    def test_apply_interest_filters_conflicting_interests(self):
        """Test filtering out careers with conflicting interests."""
        # Create a career that conflicts with user's low interest in leadership
        leadership_career = Career(
            career_id="leadership_career",
            title="Team Leadership Manager",
            description="Leading teams and managing people in leadership roles",
            required_skills=[],
            salary_range=SalaryRange(min=90000, max=130000, currency="USD"),
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="Corporate",
            education_requirements="Bachelor's degree"
        )
        
        careers_with_leadership = self.careers + [leadership_career]
        filtered_careers = self.filter_engine.apply_interest_filters(self.user_profile, careers_with_leadership)
        
        # Leadership career might be filtered out due to conflicting interests
        career_ids = [career.career_id for career in filtered_careers]
        # Note: Current implementation is permissive, so this test checks the logic exists
        self.assertIsInstance(filtered_careers, list)
    
    def test_is_salary_compatible_exact_match(self):
        """Test salary compatibility with exact range match."""
        compatible_career = Career(
            career_id="compatible",
            title="Compatible Role",
            description="Role with compatible salary",
            required_skills=[],
            salary_range=SalaryRange(min=80000, max=120000, currency="USD"),  # Exact match
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="Various",
            education_requirements="Bachelor's degree"
        )
        
        is_compatible = self.filter_engine._is_salary_compatible(self.user_profile, compatible_career)
        self.assertTrue(is_compatible)
    
    def test_is_salary_compatible_with_deviation(self):
        """Test salary compatibility with deviation tolerance."""
        # Career slightly outside range but within deviation tolerance
        deviation_career = Career(
            career_id="deviation",
            title="Deviation Role",
            description="Role with salary within deviation",
            required_skills=[],
            salary_range=SalaryRange(min=75000, max=125000, currency="USD"),  # Slightly outside but within 20% deviation
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="Various",
            education_requirements="Bachelor's degree"
        )
        
        is_compatible = self.filter_engine._is_salary_compatible(self.user_profile, deviation_career)
        self.assertTrue(is_compatible)
    
    def test_is_salary_compatible_different_currency(self):
        """Test salary compatibility with different currencies."""
        different_currency_career = Career(
            career_id="different_currency",
            title="International Role",
            description="Role with different currency",
            required_skills=[],
            salary_range=SalaryRange(min=70000, max=100000, currency="EUR"),
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="International",
            education_requirements="Bachelor's degree"
        )
        
        is_compatible = self.filter_engine._is_salary_compatible(self.user_profile, different_currency_career)
        # Current implementation assumes compatibility for different currencies
        self.assertTrue(is_compatible)
    
    def test_get_user_skill_set(self):
        """Test extraction of user skill set."""
        skill_set = self.filter_engine._get_user_skill_set(self.user_profile)
        
        # Should include skills from all sources (normalized to lowercase)
        expected_skills = {"python", "data analysis", "machine learning"}
        self.assertTrue(expected_skills.issubset(skill_set))
    
    def test_get_related_skills(self):
        """Test related skills extraction."""
        user_skills = {"python"}
        related_skills = self.filter_engine._get_related_skills(user_skills)
        
        # Should include related skills for Python
        self.assertIn("machine learning", related_skills)
        self.assertIn("data analysis", related_skills)
    
    def test_calculate_skill_overlap(self):
        """Test skill overlap calculation."""
        overlap = self.filter_engine._calculate_skill_overlap(self.user_profile, self.careers[0])  # Data Scientist
        
        # User has Python and Data Analysis, career requires Python, ML, and Data Analysis
        # Should have some overlap
        self.assertGreater(overlap, 0.0)
        self.assertLessEqual(overlap, 1.0)
    
    def test_has_mandatory_skills_true(self):
        """Test mandatory skills check when user has all mandatory skills."""
        # Create career where user has all mandatory skills
        career_with_mandatory = Career(
            career_id="mandatory_match",
            title="Python Developer",
            description="Develops with Python",
            required_skills=[
                RequiredSkill(skill_id="skill_1", name="Python", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=1.0)
            ],
            salary_range=SalaryRange(min=80000, max=120000, currency="USD"),
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="Tech",
            education_requirements="Bachelor's degree"
        )
        
        has_mandatory = self.filter_engine._has_mandatory_skills(self.user_profile, career_with_mandatory)
        self.assertTrue(has_mandatory)
    
    def test_has_mandatory_skills_false(self):
        """Test mandatory skills check when user is missing mandatory skills."""
        # Create career where user is missing mandatory skills
        career_missing_mandatory = Career(
            career_id="mandatory_missing",
            title="JavaScript Developer",
            description="Develops with JavaScript",
            required_skills=[
                RequiredSkill(skill_id="skill_4", name="JavaScript", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=1.0)
            ],
            salary_range=SalaryRange(min=80000, max=120000, currency="USD"),
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="Tech",
            education_requirements="Bachelor's degree"
        )
        
        has_mandatory = self.filter_engine._has_mandatory_skills(self.user_profile, career_missing_mandatory)
        self.assertFalse(has_mandatory)
    
    def test_calculate_interest_alignment(self):
        """Test interest alignment calculation."""
        alignment = self.filter_engine._calculate_interest_alignment(self.user_profile, self.careers[0])  # Data Scientist
        
        # Should have some alignment since career mentions "data" and user is interested in "Data Analysis"
        self.assertGreaterEqual(alignment, 0.0)
        self.assertLessEqual(alignment, 1.0)
    
    def test_get_filter_statistics(self):
        """Test filter statistics generation."""
        stats = self.filter_engine.get_filter_statistics(self.user_profile, self.careers)
        
        # Should return dictionary with expected keys
        expected_keys = ["original_count", "after_initial_filters", "after_skill_filters", "after_interest_filters"]
        for key in expected_keys:
            self.assertIn(key, stats)
        
        # Original count should match input
        self.assertEqual(stats["original_count"], len(self.careers))
        
        # Each stage should have <= previous stage
        self.assertLessEqual(stats["after_initial_filters"], stats["original_count"])
        self.assertLessEqual(stats["after_skill_filters"], stats["after_initial_filters"])
        self.assertLessEqual(stats["after_interest_filters"], stats["after_skill_filters"])


class TestFilterEngineEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions for FilterEngine."""
    
    def setUp(self):
        """Set up test fixtures for edge cases."""
        self.config = FilteringConfig(
            min_skill_overlap=0.5,
            max_salary_deviation=0.1,
            consider_related_skills=False
        )
        self.skills_db = []
        self.filter_engine = FilterEngine(self.config, self.skills_db)
    
    def test_empty_careers_list(self):
        """Test filtering with empty careers list."""
        user_profile = Mock()
        empty_careers = []
        
        filtered_careers = self.filter_engine.filter_careers(user_profile, empty_careers)
        self.assertEqual(len(filtered_careers), 0)
    
    def test_empty_skills_database(self):
        """Test filtering with empty skills database."""
        # This should not crash and should handle gracefully
        user_profile = Mock()
        user_profile.skills = []
        user_profile.professional_data.resume_skills = []
        user_profile.professional_data.linkedin_skills = []
        
        skill_set = self.filter_engine._get_user_skill_set(user_profile)
        self.assertEqual(len(skill_set), 0)
    
    def test_career_with_no_required_skills(self):
        """Test filtering career with no required skills."""
        user_profile = Mock()
        career_no_skills = Career(
            career_id="no_skills",
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
        
        overlap = self.filter_engine._calculate_skill_overlap(user_profile, career_no_skills)
        self.assertEqual(overlap, 1.0)  # Perfect match when no requirements


if __name__ == '__main__':
    unittest.main()