"""
Unit tests for prompt size validation and pre-filtering in the recommendation engine.

Tests the new functionality to prevent "prompt too long" errors by validating
prompt size and implementing more aggressive pre-filtering.
"""

import unittest
from unittest.mock import Mock, patch
import json
from datetime import datetime, timedelta

# Import the modules we're testing
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import using importlib to handle the hyphenated directory name
import importlib.util

# Load modules from recommendation-engine directory
def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Get the base path
base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'recommendation-engine')

# Load the modules
engine_module = load_module_from_path("engine", os.path.join(base_path, "engine.py"))
models_module = load_module_from_path("models", os.path.join(base_path, "models.py"))
config_module = load_module_from_path("config", os.path.join(base_path, "config.py"))

# Import the classes we need
RecommendationEngine = engine_module.RecommendationEngine
UserProfile = models_module.UserProfile
Career = models_module.Career
Skill = models_module.Skill
UserSkill = models_module.UserSkill
RequiredSkill = models_module.RequiredSkill
SalaryRange = models_module.SalaryRange
PersonalInfo = models_module.PersonalInfo
AssessmentResults = models_module.AssessmentResults
ProfessionalData = models_module.ProfessionalData
Experience = models_module.Experience
SkillLevel = models_module.SkillLevel
InterestLevel = models_module.InterestLevel
Demand = models_module.Demand
RecommendationConfig = config_module.RecommendationConfig


class TestPromptSizeValidation(unittest.TestCase):
    """Test cases for prompt size validation functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create test configuration with aggressive pre-filtering
        self.config = RecommendationConfig(
            prefilter_limit=100,  # Reduced from default 200
            max_recommendations=10,
            min_recommendations=3
        )
        
        # Create test skills database
        self.skills_db = [
            Skill(
                skill_id="skill_1",
                name="Python",
                category="Programming Language",
                related_skills=["skill_2"]
            ),
            Skill(
                skill_id="skill_2",
                name="Machine Learning",
                category="Technical Skill",
                related_skills=["skill_1"]
            )
        ]
        
        # Create recommendation engine
        self.engine = RecommendationEngine(self.config, self.skills_db)
        
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
                    "Data Analysis": InterestLevel.HIGH
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
                        description="Analyzed data using Python",
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
                )
            ],
            user_interests=["AI Ethics", "Data Privacy"]
        )
    
    def create_test_career(self, career_id: str, title: str, description_length: int = 100) -> Career:
        """Helper method to create test careers with varying description lengths."""
        description = "A" * description_length  # Create description of specified length
        
        return Career(
            career_id=career_id,
            title=title,
            description=description,
            required_skills=[
                RequiredSkill(
                    skill_id="skill_1",
                    name="Python",
                    proficiency=SkillLevel.INTERMEDIATE,
                    is_mandatory=True,
                    weight=1.0
                )
            ],
            salary_range=SalaryRange(min=80000, max=120000, currency="USD"),
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="Tech",
            education_requirements="Bachelor's degree",
            career_field="technology"
        )
    
    def test_validate_prompt_size_within_limit(self):
        """Test prompt size validation when careers fit within limit."""
        # Create a small number of careers that should fit within the limit
        careers = [
            self.create_test_career(f"career_{i}", f"Test Career {i}", 100)
            for i in range(5)
        ]
        
        validated_careers, was_truncated = self.engine._validate_prompt_size(
            self.user_profile, careers, max_size=50000
        )
        
        # Should not be truncated
        self.assertFalse(was_truncated)
        self.assertEqual(len(validated_careers), len(careers))
        self.assertEqual(validated_careers, careers)
    
    def test_validate_prompt_size_exceeds_limit(self):
        """Test prompt size validation when careers exceed limit."""
        # Create many careers with long descriptions to exceed the limit
        careers = [
            self.create_test_career(f"career_{i}", f"Test Career {i}", 1000)
            for i in range(100)
        ]
        
        validated_careers, was_truncated = self.engine._validate_prompt_size(
            self.user_profile, careers, max_size=10000  # Small limit to force truncation
        )
        
        # Should be truncated
        self.assertTrue(was_truncated)
        self.assertLess(len(validated_careers), len(careers))
        self.assertGreater(len(validated_careers), 0)
    
    def test_validate_prompt_size_empty_careers(self):
        """Test prompt size validation with empty careers list."""
        careers = []
        
        validated_careers, was_truncated = self.engine._validate_prompt_size(
            self.user_profile, careers
        )
        
        self.assertFalse(was_truncated)
        self.assertEqual(len(validated_careers), 0)
    
    def test_validate_prompt_size_single_career(self):
        """Test prompt size validation with single career."""
        careers = [self.create_test_career("career_1", "Single Career", 100)]
        
        validated_careers, was_truncated = self.engine._validate_prompt_size(
            self.user_profile, careers
        )
        
        self.assertFalse(was_truncated)
        self.assertEqual(len(validated_careers), 1)
    
    def test_validate_prompt_size_error_handling(self):
        """Test prompt size validation error handling."""
        # Create careers with problematic data that might cause JSON serialization issues
        careers = [self.create_test_career("career_1", "Test Career", 100)]
        
        # Mock JSON dumps to raise an exception
        with patch('json.dumps', side_effect=Exception("JSON error")):
            validated_careers, was_truncated = self.engine._validate_prompt_size(
                self.user_profile, careers
            )
            
            # Should fall back to conservative limit
            self.assertTrue(was_truncated or len(validated_careers) <= engine_module.MAX_CAREERS_FOR_PROMPT)
    
    def test_prefilter_limit_configuration(self):
        """Test that the prefilter limit has been reduced as expected."""
        # Check that the default configuration has the reduced prefilter limit
        self.assertEqual(self.config.prefilter_limit, 100)
        
        # Verify it's less than the original default
        default_config = RecommendationConfig()
        self.assertEqual(default_config.prefilter_limit, 100)  # Should be the new reduced value
    
    def test_prefilter_effectiveness(self):
        """Test that pre-filtering effectively reduces the number of careers."""
        # Create a large number of careers with varying relevance
        careers = []
        
        # Create highly relevant careers (should be kept)
        for i in range(20):
            career = Career(
                career_id=f"relevant_{i}",
                title=f"Python Developer {i}",
                description="Develops software using Python and machine learning",
                required_skills=[
                    RequiredSkill(
                        skill_id="skill_1",
                        name="Python",
                        proficiency=SkillLevel.INTERMEDIATE,
                        is_mandatory=True,
                        weight=1.0
                    ),
                    RequiredSkill(
                        skill_id="skill_2",
                        name="Machine Learning",
                        proficiency=SkillLevel.INTERMEDIATE,
                        is_mandatory=False,
                        weight=0.8
                    )
                ],
                salary_range=SalaryRange(min=80000, max=120000, currency="USD"),
                demand=Demand.HIGH,
                related_careers=[],
                growth_potential="Excellent",
                work_environment="Tech companies",
                education_requirements="Bachelor's degree",
                career_field="technology"
            )
            careers.append(career)
        
        # Create less relevant careers (should be filtered out)
        for i in range(80):
            career = Career(
                career_id=f"irrelevant_{i}",
                title=f"Unrelated Job {i}",
                description="Job that has nothing to do with user's skills or interests",
                required_skills=[
                    RequiredSkill(
                        skill_id="skill_unrelated",
                        name="Unrelated Skill",
                        proficiency=SkillLevel.EXPERT,
                        is_mandatory=True,
                        weight=1.0
                    )
                ],
                salary_range=SalaryRange(min=30000, max=50000, currency="USD"),
                demand=Demand.LOW,
                related_careers=[],
                growth_potential="Limited",
                work_environment="Various",
                education_requirements="High school",
                career_field="other"
            )
            careers.append(career)
        
        # Create summarized profile
        summarized_profile = self.engine._preprocess_user_profile(self.user_profile)
        
        # Apply pre-filtering
        filtered_careers = self.engine._prefilter_careers(summarized_profile, careers)
        
        # Should significantly reduce the number of careers
        self.assertLessEqual(len(filtered_careers), self.config.prefilter_limit)
        self.assertLess(len(filtered_careers), len(careers))
        
        # Should prioritize relevant careers
        filtered_ids = [career.career_id for career in filtered_careers]
        relevant_in_filtered = sum(1 for career_id in filtered_ids if career_id.startswith("relevant_"))
        irrelevant_in_filtered = sum(1 for career_id in filtered_ids if career_id.startswith("irrelevant_"))
        
        # Should have more relevant than irrelevant careers
        self.assertGreater(relevant_in_filtered, irrelevant_in_filtered)
    
    @patch('recommendation-engine.engine.logger')
    def test_prompt_validation_logging(self, mock_logger):
        """Test that appropriate warnings are logged during prompt validation."""
        # Create careers that will exceed the limit
        careers = [
            self.create_test_career(f"career_{i}", f"Test Career {i}", 1000)
            for i in range(50)
        ]
        
        # Validate with small limit to force truncation
        self.engine._validate_prompt_size(self.user_profile, careers, max_size=5000)
        
        # Check that warning was logged
        mock_logger.warning.assert_called()
        warning_calls = [call for call in mock_logger.warning.call_args_list 
                        if "exceeds limit" in str(call) or "Truncated careers list" in str(call)]
        self.assertGreater(len(warning_calls), 0)
    
    def test_integration_with_get_recommendations(self):
        """Test that the prompt validation integrates properly with the main recommendation flow."""
        # Create a moderate number of careers
        careers = [
            self.create_test_career(f"career_{i}", f"Test Career {i}", 200)
            for i in range(30)
        ]
        
        # Get recommendations (this should use the new validation internally)
        recommendations = self.engine.get_recommendations(
            self.user_profile, careers, limit=5, exploration_level=3
        )
        
        # Should return recommendations without errors
        self.assertIsInstance(recommendations, list)
        self.assertLessEqual(len(recommendations), 5)


class TestPreprocessingEffectiveness(unittest.TestCase):
    """Test cases for user profile preprocessing effectiveness."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = RecommendationEngine()
        
        # Create user profile with extensive data
        self.user_profile = UserProfile(
            user_id="test_user",
            personal_info=PersonalInfo(
                age=30,
                location="New York, NY",
                salary_expectations=SalaryRange(min=90000, max=150000, currency="USD"),
                willing_to_relocate=True,
                preferred_work_style="remote"
            ),
            assessment_results=AssessmentResults(
                personality_traits=["Analytical", "Creative", "Detail-Oriented", "Leadership"],
                work_values=["Autonomy", "Innovation", "Work-Life Balance", "Growth"],
                interests={
                    "Technology": InterestLevel.VERY_HIGH,
                    "Data Science": InterestLevel.HIGH,
                    "Management": InterestLevel.MEDIUM,
                    "Teaching": InterestLevel.LOW
                }
            ),
            professional_data=ProfessionalData(
                resume_skills=["Python", "SQL", "Machine Learning", "Data Analysis", "Project Management"],
                linkedin_skills=["Python", "R", "Tableau", "Leadership", "Communication"],
                experience=[
                    Experience(
                        title="Senior Data Scientist",
                        company="Tech Corp",
                        duration_years=3.0,
                        description="Led data science projects and managed a team of analysts",
                        skills_used=["Python", "Machine Learning", "Leadership"]
                    ),
                    Experience(
                        title="Data Analyst",
                        company="Previous Corp",
                        duration_years=2.0,
                        description="Analyzed business data and created reports",
                        skills_used=["SQL", "Data Analysis", "Tableau"]
                    )
                ],
                education="Master's in Data Science",
                certifications=["AWS Certified", "Google Analytics"]
            ),
            skills=[
                UserSkill(
                    skill_id="skill_1",
                    name="Python",
                    level=SkillLevel.EXPERT,
                    years_experience=5.0,
                    is_certified=True,
                    last_used=datetime.utcnow()
                ),
                UserSkill(
                    skill_id="skill_2",
                    name="Machine Learning",
                    level=SkillLevel.ADVANCED,
                    years_experience=3.0,
                    is_certified=False,
                    last_used=datetime.utcnow() - timedelta(days=30)
                )
            ],
            user_interests=["AI Ethics", "Data Privacy", "Open Source", "Mentoring"]
        )
    
    def test_preprocess_user_profile_summarization(self):
        """Test that user profile preprocessing creates appropriate summary."""
        summary = self.engine._preprocess_user_profile(self.user_profile)
        
        # Check that summary contains expected keys
        expected_keys = [
            "key_skills", "soft_skills", "experience_years", "primary_industries",
            "career_goals", "interests", "work_preferences", "salary_range",
            "education_level", "current_role", "location", "resume_summary"
        ]
        
        for key in expected_keys:
            self.assertIn(key, summary)
        
        # Check that skills are limited appropriately
        self.assertLessEqual(len(summary["key_skills"]), 10)
        self.assertLessEqual(len(summary["interests"]), 5)
        
        # Check that experience years is calculated
        self.assertIsInstance(summary["experience_years"], (int, float))
        self.assertGreater(summary["experience_years"], 0)
    
    def test_preprocess_user_profile_resume_truncation(self):
        """Test that long resume text is properly truncated."""
        # Create user profile with very long resume text
        long_resume = "A" * 1000  # 1000 character resume
        
        user_with_long_resume = self.user_profile.copy()
        user_with_long_resume.resumeText = long_resume
        
        summary = self.engine._preprocess_user_profile(user_with_long_resume)
        
        # Resume should be truncated to 500 characters + "..."
        self.assertLessEqual(len(summary["resume_summary"]), 503)
        if len(long_resume) > 500:
            self.assertTrue(summary["resume_summary"].endswith("..."))


if __name__ == '__main__':
    unittest.main()