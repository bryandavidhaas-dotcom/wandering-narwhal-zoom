"""
Unit tests for the scoring logic in the recommendation engine.

Tests the ScoringEngine class and its methods for scoring career recommendations
based on skill matching, interest alignment, salary compatibility, and experience.
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Import the modules we're testing
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from recommendation_engine.scoring import ScoringEngine
from recommendation_engine.models import (
    UserProfile, Career, UserSkill, RequiredSkill, SalaryRange,
    PersonalInfo, AssessmentResults, ProfessionalData, Experience,
    SkillLevel, InterestLevel, Demand, RecommendationScore
)
from recommendation_engine.config import ScoringConfig, ScoringWeights


class TestScoringEngine(unittest.TestCase):
    """Test cases for the ScoringEngine class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create test configuration
        self.scoring_config = ScoringConfig(
            certification_bonus=0.1,
            recent_experience_bonus=0.05,
            mandatory_skill_penalty=0.3
        )
        
        self.scoring_weights = ScoringWeights(
            skill_match=0.4,
            interest_match=0.3,
            salary_compatibility=0.2,
            experience_match=0.1
        )
        
        # Create scoring engine
        self.scoring_engine = ScoringEngine(self.scoring_config, self.scoring_weights)
        
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
                    "Machine Learning": InterestLevel.MEDIUM,
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
                        duration_years=2.5,
                        description="Analyzed customer data",
                        skills_used=["Python", "Data Analysis"]
                    ),
                    Experience(
                        title="Junior Developer",
                        company="StartupXYZ",
                        duration_years=1.0,
                        description="Developed applications",
                        skills_used=["Python"]
                    )
                ],
                education="Bachelor's in Computer Science",
                certifications=["AWS Cloud Practitioner"]
            ),
            skills=[
                UserSkill(
                    skill_id="skill_1",
                    name="Python",
                    level=SkillLevel.ADVANCED,
                    years_experience=3.5,
                    is_certified=True,
                    last_used=datetime.utcnow() - timedelta(days=1)
                ),
                UserSkill(
                    skill_id="skill_2",
                    name="Machine Learning",
                    level=SkillLevel.INTERMEDIATE,
                    years_experience=1.0,
                    is_certified=False,
                    last_used=datetime.utcnow() - timedelta(days=30)
                ),
                UserSkill(
                    skill_id="skill_3",
                    name="Data Analysis",
                    level=SkillLevel.ADVANCED,
                    years_experience=2.5,
                    is_certified=False,
                    last_used=datetime.utcnow() - timedelta(days=5)
                )
            ],
            user_interests=["AI Ethics", "Data Privacy"]
        )
        
        # Create test career
        self.test_career = Career(
            career_id="career_1",
            title="Data Scientist",
            description="Analyzes complex data using Python and machine learning to extract insights",
            required_skills=[
                RequiredSkill(skill_id="skill_1", name="Python", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_2", name="Machine Learning", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.8),
                RequiredSkill(skill_id="skill_3", name="Data Analysis", proficiency=SkillLevel.ADVANCED, is_mandatory=False, weight=0.7)
            ],
            salary_range=SalaryRange(min=90000, max=140000, currency="USD"),
            demand=Demand.HIGH,
            related_careers=[],
            growth_potential="Excellent growth potential",
            work_environment="Tech companies, startups",
            education_requirements="Bachelor's in Computer Science or related field"
        )
    
    def test_score_career_complete(self):
        """Test complete career scoring."""
        score = self.scoring_engine.score_career(self.user_profile, self.test_career)
        
        # Should return RecommendationScore object
        self.assertIsInstance(score, RecommendationScore)
        self.assertEqual(score.career_id, "career_1")
        
        # Total score should be between 0 and 1
        self.assertGreaterEqual(score.total_score, 0.0)
        self.assertLessEqual(score.total_score, 1.0)
        
        # Individual scores should be between 0 and 1
        self.assertGreaterEqual(score.skill_match_score, 0.0)
        self.assertLessEqual(score.skill_match_score, 1.0)
        self.assertGreaterEqual(score.interest_match_score, 0.0)
        self.assertLessEqual(score.interest_match_score, 1.0)
        self.assertGreaterEqual(score.salary_compatibility_score, 0.0)
        self.assertLessEqual(score.salary_compatibility_score, 1.0)
        self.assertGreaterEqual(score.experience_match_score, 0.0)
        self.assertLessEqual(score.experience_match_score, 1.0)
        
        # Should have breakdown details
        self.assertIsInstance(score.breakdown, dict)
        self.assertIn("skill_details", score.breakdown)
        self.assertIn("interest_details", score.breakdown)
        self.assertIn("salary_details", score.breakdown)
        self.assertIn("experience_details", score.breakdown)
    
    def test_score_multiple_careers(self):
        """Test scoring multiple careers and sorting."""
        # Create additional test careers
        career_2 = Career(
            career_id="career_2",
            title="Web Developer",
            description="Develops web applications using JavaScript",
            required_skills=[
                RequiredSkill(skill_id="skill_4", name="JavaScript", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0)
            ],
            salary_range=SalaryRange(min=70000, max=110000, currency="USD"),
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good growth potential",
            work_environment="Various industries",
            education_requirements="Bachelor's degree"
        )
        
        careers = [self.test_career, career_2]
        scores = self.scoring_engine.score_multiple_careers(self.user_profile, careers)
        
        # Should return list of scores
        self.assertIsInstance(scores, list)
        self.assertEqual(len(scores), 2)
        
        # Should be sorted by total score (descending)
        for i in range(len(scores) - 1):
            self.assertGreaterEqual(scores[i].total_score, scores[i + 1].total_score)
    
    def test_calculate_skill_match_score_perfect_match(self):
        """Test skill matching with perfect match."""
        # Create career that perfectly matches user skills
        perfect_career = Career(
            career_id="perfect",
            title="Python Data Analyst",
            description="Uses Python for data analysis",
            required_skills=[
                RequiredSkill(skill_id="skill_1", name="Python", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_3", name="Data Analysis", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=1.0)
            ],
            salary_range=SalaryRange(min=80000, max=120000, currency="USD"),
            demand=Demand.HIGH,
            related_careers=[],
            growth_potential="Good",
            work_environment="Tech",
            education_requirements="Bachelor's"
        )
        
        skill_score = self.scoring_engine._calculate_skill_match_score(self.user_profile, perfect_career)
        
        # Should have high skill score since user exceeds requirements
        self.assertGreater(skill_score, 0.8)
    
    def test_calculate_skill_match_score_missing_mandatory(self):
        """Test skill matching with missing mandatory skills."""
        # Create career with mandatory skill user doesn't have
        missing_mandatory_career = Career(
            career_id="missing_mandatory",
            title="JavaScript Developer",
            description="Develops with JavaScript",
            required_skills=[
                RequiredSkill(skill_id="skill_4", name="JavaScript", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=1.0)
            ],
            salary_range=SalaryRange(min=80000, max=120000, currency="USD"),
            demand=Demand.HIGH,
            related_careers=[],
            growth_potential="Good",
            work_environment="Tech",
            education_requirements="Bachelor's"
        )
        
        skill_score = self.scoring_engine._calculate_skill_match_score(self.user_profile, missing_mandatory_career)
        
        # Should have low skill score due to missing mandatory skill
        self.assertLess(skill_score, 0.5)
    
    def test_calculate_skill_match_score_no_requirements(self):
        """Test skill matching with no skill requirements."""
        no_requirements_career = Career(
            career_id="no_requirements",
            title="General Role",
            description="Role with no specific requirements",
            required_skills=[],
            salary_range=SalaryRange(min=80000, max=120000, currency="USD"),
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="Various",
            education_requirements="High school"
        )
        
        skill_score = self.scoring_engine._calculate_skill_match_score(self.user_profile, no_requirements_career)
        
        # Should return perfect score when no requirements
        self.assertEqual(skill_score, 1.0)
    
    def test_calculate_interest_match_score_high_alignment(self):
        """Test interest matching with high alignment."""
        # Career description contains user's interests
        interest_score = self.scoring_engine._calculate_interest_match_score(self.user_profile, self.test_career)
        
        # Should have some positive alignment since career mentions "data" and user is interested in "Data Analysis"
        self.assertGreater(interest_score, 0.0)
    
    def test_calculate_interest_match_score_no_interests(self):
        """Test interest matching when user has no specified interests."""
        # Create user profile without interests
        user_no_interests = UserProfile(
            user_id="no_interests",
            personal_info=self.user_profile.personal_info,
            assessment_results=AssessmentResults(
                personality_traits=["Analytical"],
                work_values=["Autonomy"],
                interests={}
            ),
            professional_data=self.user_profile.professional_data,
            skills=self.user_profile.skills,
            user_interests=[]
        )
        
        interest_score = self.scoring_engine._calculate_interest_match_score(user_no_interests, self.test_career)
        
        # Should return neutral score (0.5) when no interests specified
        self.assertEqual(interest_score, 0.5)
    
    def test_calculate_salary_compatibility_score_perfect_overlap(self):
        """Test salary compatibility with perfect overlap."""
        # Create career with salary range that perfectly overlaps user expectations
        perfect_salary_career = Career(
            career_id="perfect_salary",
            title="Perfect Salary Role",
            description="Role with perfect salary match",
            required_skills=[],
            salary_range=SalaryRange(min=80000, max=120000, currency="USD"),  # Exact match
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="Various",
            education_requirements="Bachelor's"
        )
        
        salary_score = self.scoring_engine._calculate_salary_compatibility_score(self.user_profile, perfect_salary_career)
        
        # Should have high compatibility score
        self.assertGreater(salary_score, 0.8)
    
    def test_calculate_salary_compatibility_score_no_overlap_too_low(self):
        """Test salary compatibility when career pays too little."""
        low_salary_career = Career(
            career_id="low_salary",
            title="Low Salary Role",
            description="Role with low salary",
            required_skills=[],
            salary_range=SalaryRange(min=40000, max=60000, currency="USD"),  # Below user expectations
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="Various",
            education_requirements="Bachelor's"
        )
        
        salary_score = self.scoring_engine._calculate_salary_compatibility_score(self.user_profile, low_salary_career)
        
        # Should have low compatibility score
        self.assertLess(salary_score, 0.5)
    
    def test_calculate_salary_compatibility_score_higher_than_expected(self):
        """Test salary compatibility when career pays more than expected."""
        high_salary_career = Career(
            career_id="high_salary",
            title="High Salary Role",
            description="Role with high salary",
            required_skills=[],
            salary_range=SalaryRange(min=150000, max=200000, currency="USD"),  # Above user expectations
            demand=Demand.MEDIUM,
            related_careers=[],
            growth_potential="Good",
            work_environment="Various",
            education_requirements="Bachelor's"
        )
        
        salary_score = self.scoring_engine._calculate_salary_compatibility_score(self.user_profile, high_salary_career)
        
        # Should have decent compatibility score (less penalty for higher pay)
        self.assertGreater(salary_score, 0.3)
    
    def test_calculate_salary_compatibility_score_different_currency(self):
        """Test salary compatibility with different currency."""
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
            education_requirements="Bachelor's"
        )
        
        salary_score = self.scoring_engine._calculate_salary_compatibility_score(self.user_profile, different_currency_career)
        
        # Should have slight penalty for currency mismatch
        self.assertEqual(salary_score, 0.8)
    
    def test_calculate_salary_compatibility_score_no_expectations(self):
        """Test salary compatibility when user has no salary expectations."""
        user_no_salary = UserProfile(
            user_id="no_salary",
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
        
        salary_score = self.scoring_engine._calculate_salary_compatibility_score(user_no_salary, self.test_career)
        
        # Should return perfect score when no expectations
        self.assertEqual(salary_score, 1.0)
    
    def test_calculate_experience_match_score(self):
        """Test experience level matching."""
        experience_score = self.scoring_engine._calculate_experience_match_score(self.user_profile, self.test_career)
        
        # User has 3.5 years total experience (junior to mid level)
        self.assertGreaterEqual(experience_score, 0.0)
        self.assertLessEqual(experience_score, 1.0)
    
    def test_calculate_proficiency_match_exact_match(self):
        """Test proficiency matching with exact level match."""
        match_score = self.scoring_engine._calculate_proficiency_match(SkillLevel.ADVANCED, SkillLevel.ADVANCED)
        self.assertEqual(match_score, 1.0)
    
    def test_calculate_proficiency_match_user_exceeds(self):
        """Test proficiency matching when user exceeds requirement."""
        match_score = self.scoring_engine._calculate_proficiency_match(SkillLevel.EXPERT, SkillLevel.INTERMEDIATE)
        self.assertEqual(match_score, 1.0)
    
    def test_calculate_proficiency_match_user_below(self):
        """Test proficiency matching when user is below requirement."""
        match_score = self.scoring_engine._calculate_proficiency_match(SkillLevel.BEGINNER, SkillLevel.ADVANCED)
        
        # Should have penalty for being 2 levels below (2 * 0.25 = 0.5 penalty)
        expected_score = 1.0 - (2 * 0.25)
        self.assertEqual(match_score, expected_score)
    
    def test_is_recent_experience_true(self):
        """Test recent experience check for recent skill usage."""
        recent_date = datetime.utcnow() - timedelta(days=30)
        is_recent = self.scoring_engine._is_recent_experience(recent_date)
        self.assertTrue(is_recent)
    
    def test_is_recent_experience_false(self):
        """Test recent experience check for old skill usage."""
        old_date = datetime.utcnow() - timedelta(days=200)
        is_recent = self.scoring_engine._is_recent_experience(old_date)
        self.assertFalse(is_recent)
    
    def test_is_recent_experience_none(self):
        """Test recent experience check with None date."""
        is_recent = self.scoring_engine._is_recent_experience(None)
        self.assertFalse(is_recent)
    
    def test_interest_level_to_weight(self):
        """Test conversion of interest levels to weights."""
        weights = {
            InterestLevel.LOW: 0.25,
            InterestLevel.MEDIUM: 0.5,
            InterestLevel.HIGH: 0.75,
            InterestLevel.VERY_HIGH: 1.0
        }
        
        for level, expected_weight in weights.items():
            weight = self.scoring_engine._interest_level_to_weight(level)
            self.assertEqual(weight, expected_weight)
    
    def test_get_skill_score_details(self):
        """Test detailed skill score breakdown."""
        details = self.scoring_engine._get_skill_score_details(self.user_profile, self.test_career)
        
        # Should have expected structure
        self.assertIn("matched_skills", details)
        self.assertIn("missing_mandatory", details)
        self.assertIn("missing_preferred", details)
        
        # Should have matched skills (Python, Machine Learning, Data Analysis)
        self.assertGreater(len(details["matched_skills"]), 0)
    
    def test_get_interest_score_details(self):
        """Test detailed interest score breakdown."""
        details = self.scoring_engine._get_interest_score_details(self.user_profile, self.test_career)
        
        # Should have expected structure
        self.assertIn("matched_interests", details)
        self.assertIn("user_interests", details)
        self.assertIn("additional_interests", details)
        
        # Should include user's interests
        self.assertIn("Technology", details["user_interests"])
        self.assertIn("Data Analysis", details["user_interests"])
    
    def test_get_salary_score_details(self):
        """Test detailed salary score breakdown."""
        details = self.scoring_engine._get_salary_score_details(self.user_profile, self.test_career)
        
        # Should have expected structure
        self.assertIn("user_expectations", details)
        self.assertIn("career_range", details)
        self.assertIn("compatibility", details)
        
        # Should have user expectations
        self.assertIsNotNone(details["user_expectations"])
        self.assertEqual(details["user_expectations"]["min"], 80000)
        self.assertEqual(details["user_expectations"]["max"], 120000)
        
        # Should determine compatibility
        self.assertIn(details["compatibility"], ["compatible", "too_low", "higher_than_expected", "different_currency"])
    
    def test_get_experience_score_details(self):
        """Test detailed experience score breakdown."""
        details = self.scoring_engine._get_experience_score_details(self.user_profile, self.test_career)
        
        # Should have expected structure
        self.assertIn("total_years", details)
        self.assertIn("experience_level", details)
        self.assertIn("relevant_experience", details)
        
        # Should calculate total years correctly
        expected_total = 2.5 + 1.0  # From the two experiences
        self.assertEqual(details["total_years"], expected_total)
        
        # Should have relevant experience entries
        self.assertEqual(len(details["relevant_experience"]), 2)
    
    def test_get_experience_level(self):
        """Test experience level categorization."""
        test_cases = [
            (0.5, "entry"),
            (2.0, "junior"),
            (5.0, "mid"),
            (10.0, "senior"),
            (15.0, "expert")
        ]
        
        for years, expected_level in test_cases:
            level = self.scoring_engine._get_experience_level(years)
            self.assertEqual(level, expected_level)


class TestScoringEngineEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions for ScoringEngine."""
    
    def setUp(self):
        """Set up test fixtures for edge cases."""
        self.scoring_config = ScoringConfig(
            certification_bonus=0.1,
            recent_experience_bonus=0.05,
            mandatory_skill_penalty=0.3
        )
        
        self.scoring_weights = ScoringWeights(
            skill_match=0.4,
            interest_match=0.3,
            salary_compatibility=0.2,
            experience_match=0.1
        )
        
        self.scoring_engine = ScoringEngine(self.scoring_config, self.scoring_weights)
    
    def test_score_clamping(self):
        """Test that scores are properly clamped to [0, 1] range."""
        # Create a mock score that would exceed 1.0
        user_profile = Mock()
        career = Mock()
        
        # Mock individual scoring methods to return values that would sum > 1.0
        with patch.object(self.scoring_engine, '_calculate_skill_match_score', return_value=1.0), \
             patch.object(self.scoring_engine, '_calculate_interest_match_score', return_value=1.0), \
             patch.object(self.scoring_engine, '_calculate_salary_compatibility_score', return_value=1.0), \
             patch.object(self.scoring_engine, '_calculate_experience_match_score', return_value=1.0), \
             patch.object(self.scoring_engine, '_get_skill_score_details', return_value={}), \
             patch.object(self.scoring_engine, '_get_interest_score_details', return_value={}), \
             patch.object(self.scoring_engine, '_get_salary_score_details', return_value={}), \
             patch.object(self.scoring_engine, '_get_experience_score_details', return_value={}):
            
            career.career_id = "test_career"
            score = self.scoring_engine.score_career(user_profile, career)
            
            # Total score should be clamped to 1.0
            self.assertLessEqual(score.total_score, 1.0)
            self.assertGreaterEqual(score.total_score, 0.0)


if __name__ == '__main__':
    unittest.main()