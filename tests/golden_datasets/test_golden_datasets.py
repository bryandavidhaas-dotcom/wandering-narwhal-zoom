"""
Golden dataset tests for the recommendation engine.

Tests the recommendation engine against curated golden datasets
to ensure consistent and expected behavior.
"""

import unittest
import json
import os
from datetime import datetime
from typing import Dict, List, Any

# Import the modules we're testing
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from recommendation_engine.engine import RecommendationEngine
from recommendation_engine.models import (
    UserProfile, PersonalInfo, AssessmentResults, ProfessionalData,
    Experience, UserSkill, SalaryRange, SkillLevel, InterestLevel
)
from recommendation_engine.mock_data import MOCK_SKILLS, MOCK_CAREERS


class TestGoldenDatasets(unittest.TestCase):
    """Test cases for golden dataset validation."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.engine = RecommendationEngine()
        self.skills = MOCK_SKILLS
        self.careers = MOCK_CAREERS
        self.golden_datasets_dir = os.path.dirname(__file__)
    
    def load_golden_dataset(self, filename: str) -> Dict[str, Any]:
        """Load a golden dataset from JSON file."""
        filepath = os.path.join(self.golden_datasets_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def convert_json_to_user_profile(self, json_profile: Dict[str, Any]) -> UserProfile:
        """Convert JSON user profile to UserProfile object."""
        # Convert salary expectations
        salary_exp = None
        if json_profile["personal_info"].get("salary_expectations"):
            salary_data = json_profile["personal_info"]["salary_expectations"]
            salary_exp = SalaryRange(
                min=salary_data["min"],
                max=salary_data["max"],
                currency=salary_data["currency"]
            )
        
        # Convert personal info
        personal_info = PersonalInfo(
            age=json_profile["personal_info"]["age"],
            location=json_profile["personal_info"]["location"],
            salary_expectations=salary_exp,
            willing_to_relocate=json_profile["personal_info"]["willing_to_relocate"],
            preferred_work_style=json_profile["personal_info"]["preferred_work_style"]
        )
        
        # Convert interests
        interests = {}
        for interest, level_str in json_profile["assessment_results"]["interests"].items():
            level_map = {
                "low": InterestLevel.LOW,
                "medium": InterestLevel.MEDIUM,
                "high": InterestLevel.HIGH,
                "very_high": InterestLevel.VERY_HIGH
            }
            interests[interest] = level_map[level_str]
        
        # Convert assessment results
        assessment_results = AssessmentResults(
            personality_traits=json_profile["assessment_results"]["personality_traits"],
            work_values=json_profile["assessment_results"]["work_values"],
            interests=interests
        )
        
        # Convert experience
        experiences = []
        for exp_data in json_profile["professional_data"]["experience"]:
            experience = Experience(
                title=exp_data["title"],
                company=exp_data["company"],
                duration_years=exp_data["duration_years"],
                description=exp_data["description"],
                skills_used=exp_data["skills_used"]
            )
            experiences.append(experience)
        
        # Convert professional data
        professional_data = ProfessionalData(
            resume_skills=json_profile["professional_data"]["resume_skills"],
            linkedin_skills=json_profile["professional_data"]["linkedin_skills"],
            experience=experiences,
            education=json_profile["professional_data"]["education"],
            certifications=json_profile["professional_data"]["certifications"]
        )
        
        # Convert skills
        skills = []
        for skill_data in json_profile["skills"]:
            level_map = {
                "beginner": SkillLevel.BEGINNER,
                "intermediate": SkillLevel.INTERMEDIATE,
                "advanced": SkillLevel.ADVANCED,
                "expert": SkillLevel.EXPERT
            }
            
            last_used = None
            if skill_data.get("last_used"):
                last_used = datetime.fromisoformat(skill_data["last_used"])
            
            skill = UserSkill(
                skill_id=skill_data["skill_id"],
                name=skill_data["name"],
                level=level_map[skill_data["level"]],
                years_experience=skill_data["years_experience"],
                is_certified=skill_data["is_certified"],
                last_used=last_used
            )
            skills.append(skill)
        
        # Create user profile
        return UserProfile(
            user_id=json_profile["user_id"],
            personal_info=personal_info,
            assessment_results=assessment_results,
            professional_data=professional_data,
            skills=skills,
            user_interests=json_profile["user_interests"]
        )
    
    def validate_recommendation_against_expected(self, recommendation, expected):
        """Validate a recommendation against expected results."""
        # Check career ID match
        if expected.get("career_id"):
            self.assertEqual(recommendation.career.career_id, expected["career_id"])
        
        # Check category
        if expected.get("expected_category"):
            expected_category_map = {
                "safe_zone": "SAFE_ZONE",
                "stretch_zone": "STRETCH_ZONE", 
                "adventure_zone": "ADVENTURE_ZONE"
            }
            expected_category = expected_category_map[expected["expected_category"]]
            self.assertEqual(recommendation.category.name, expected_category)
        
        # Check score range
        if expected.get("expected_score_range"):
            score_range = expected["expected_score_range"]
            self.assertGreaterEqual(recommendation.score.total_score, score_range["min"])
            self.assertLessEqual(recommendation.score.total_score, score_range["max"])
        
        # Check reasons (partial matching)
        if expected.get("expected_reasons"):
            recommendation_reasons_text = " ".join(recommendation.reasons).lower()
            
            # Check that at least some expected reason concepts are present
            reason_matches = 0
            for expected_reason in expected["expected_reasons"]:
                # Extract key concepts from expected reason
                key_concepts = self.extract_key_concepts(expected_reason.lower())
                
                # Check if any key concepts appear in actual reasons
                for concept in key_concepts:
                    if concept in recommendation_reasons_text:
                        reason_matches += 1
                        break
            
            # Should have at least 50% of expected reason concepts
            min_matches = max(1, len(expected["expected_reasons"]) // 2)
            self.assertGreaterEqual(reason_matches, min_matches,
                f"Expected at least {min_matches} reason matches, got {reason_matches}. "
                f"Expected reasons: {expected['expected_reasons']}, "
                f"Actual reasons: {recommendation.reasons}")
    
    def extract_key_concepts(self, reason_text: str) -> List[str]:
        """Extract key concepts from a reason text for matching."""
        # Simple keyword extraction - could be enhanced with NLP
        key_concepts = []
        
        # Skill-related concepts
        if "skills" in reason_text:
            key_concepts.append("skills")
        if "python" in reason_text:
            key_concepts.append("python")
        if "sql" in reason_text:
            key_concepts.append("sql")
        if "machine learning" in reason_text:
            key_concepts.append("machine learning")
        
        # Category-related concepts
        if "low risk" in reason_text:
            key_concepts.append("low risk")
        if "additional skill development" in reason_text:
            key_concepts.append("skill development")
        if "exciting opportunity" in reason_text:
            key_concepts.append("exciting opportunity")
        
        # Interest-related concepts
        if "interests" in reason_text:
            key_concepts.append("interests")
        if "aligns" in reason_text:
            key_concepts.append("aligns")
        
        # Salary-related concepts
        if "salary" in reason_text:
            key_concepts.append("salary")
        if "compensation" in reason_text:
            key_concepts.append("compensation")
        
        # Experience-related concepts
        if "experience" in reason_text:
            key_concepts.append("experience")
        
        return key_concepts if key_concepts else [reason_text.split()[0]]  # Fallback to first word
    
    def test_data_analyst_golden_dataset(self):
        """Test the data analyst golden dataset."""
        # Load golden dataset
        dataset = self.load_golden_dataset("data_analyst_profile.json")
        
        # Convert to user profile
        user_profile = self.convert_json_to_user_profile(dataset["user_profile"])
        
        # Get recommendations
        recommendations = self.engine.get_recommendations(
            user_profile, self.careers, self.skills
        )
        
        # Validate against criteria
        validation_criteria = dataset["validation_criteria"]
        
        # Check minimum and maximum recommendations
        self.assertGreaterEqual(len(recommendations), validation_criteria["minimum_recommendations"])
        self.assertLessEqual(len(recommendations), validation_criteria["maximum_recommendations"])
        
        # Check required categories are present
        present_categories = {rec.category.name.lower() for rec in recommendations}
        for required_category in validation_criteria["required_categories"]:
            self.assertIn(required_category, present_categories,
                f"Required category '{required_category}' not found in recommendations")
        
        # Check score distribution
        score_dist = validation_criteria["score_distribution"]
        for rec in recommendations:
            category_name = rec.category.name.lower()
            if category_name == "safe_zone":
                self.assertGreaterEqual(rec.score.total_score, score_dist["safe_zone_min_score"])
            elif category_name == "stretch_zone":
                self.assertGreaterEqual(rec.score.total_score, score_dist["stretch_zone_min_score"])
            elif category_name == "adventure_zone":
                self.assertGreaterEqual(rec.score.total_score, score_dist["adventure_zone_min_score"])
        
        # Check reason validation
        reason_validation = validation_criteria["reason_validation"]
        for rec in recommendations:
            self.assertGreaterEqual(len(rec.reasons), reason_validation["min_reasons_per_recommendation"])
            self.assertLessEqual(len(rec.reasons), reason_validation["max_reasons_per_recommendation"])
        
        # Validate specific expected recommendations (if any match by career type)
        expected_recommendations = dataset["expected_recommendations"]
        
        # Create a mapping of career titles to recommendations for easier lookup
        rec_by_title = {}
        for rec in recommendations:
            title_key = rec.career.title.lower().replace(" ", "_")
            rec_by_title[title_key] = rec
        
        # Check expected recommendations that we can find
        for expected in expected_recommendations:
            career_id = expected["career_id"]
            
            # Try to find matching recommendation by career ID or similar title
            matching_rec = None
            for rec in recommendations:
                if (rec.career.career_id == career_id or 
                    career_id.replace("_", " ") in rec.career.title.lower()):
                    matching_rec = rec
                    break
            
            if matching_rec:
                # Validate this specific recommendation
                try:
                    self.validate_recommendation_against_expected(matching_rec, expected)
                except AssertionError as e:
                    # Add context about which expected recommendation failed
                    raise AssertionError(f"Validation failed for expected recommendation '{career_id}': {e}")
    
    def test_golden_dataset_consistency(self):
        """Test that golden datasets produce consistent results across multiple runs."""
        dataset = self.load_golden_dataset("data_analyst_profile.json")
        user_profile = self.convert_json_to_user_profile(dataset["user_profile"])
        
        # Run recommendations multiple times
        results = []
        for _ in range(3):
            recommendations = self.engine.get_recommendations(
                user_profile, self.careers, self.skills
            )
            results.append(recommendations)
        
        # Check consistency
        self.assertEqual(len(results[0]), len(results[1]))
        self.assertEqual(len(results[1]), len(results[2]))
        
        # Check that top recommendations are consistent
        for i in range(min(3, len(results[0]))):  # Check top 3 recommendations
            career_id_0 = results[0][i].career.career_id
            career_id_1 = results[1][i].career.career_id
            career_id_2 = results[2][i].career.career_id
            
            self.assertEqual(career_id_0, career_id_1)
            self.assertEqual(career_id_1, career_id_2)
    
    def test_golden_dataset_file_format(self):
        """Test that golden dataset files have correct format."""
        dataset = self.load_golden_dataset("data_analyst_profile.json")
        
        # Check required top-level keys
        required_keys = ["user_profile", "expected_recommendations", "validation_criteria", "test_metadata"]
        for key in required_keys:
            self.assertIn(key, dataset, f"Missing required key: {key}")
        
        # Check user profile structure
        user_profile = dataset["user_profile"]
        required_profile_keys = ["user_id", "personal_info", "assessment_results", "professional_data", "skills"]
        for key in required_profile_keys:
            self.assertIn(key, user_profile, f"Missing required user profile key: {key}")
        
        # Check expected recommendations structure
        expected_recs = dataset["expected_recommendations"]
        self.assertIsInstance(expected_recs, list)
        self.assertGreater(len(expected_recs), 0)
        
        for expected_rec in expected_recs:
            self.assertIn("career_id", expected_rec)
            self.assertIn("expected_category", expected_rec)
            self.assertIn("rationale", expected_rec)


class TestGoldenDatasetRunner(unittest.TestCase):
    """Test runner for all golden datasets in the directory."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = RecommendationEngine()
        self.skills = MOCK_SKILLS
        self.careers = MOCK_CAREERS
        self.golden_datasets_dir = os.path.dirname(__file__)
    
    def test_all_golden_datasets(self):
        """Run tests against all golden dataset files."""
        # Find all JSON files in the golden datasets directory
        json_files = [f for f in os.listdir(self.golden_datasets_dir) 
                     if f.endswith('.json') and f != 'test_golden_datasets.py']
        
        self.assertGreater(len(json_files), 0, "No golden dataset files found")
        
        for json_file in json_files:
            with self.subTest(dataset=json_file):
                # Load and validate each dataset
                try:
                    with open(os.path.join(self.golden_datasets_dir, json_file), 'r') as f:
                        dataset = json.load(f)
                    
                    # Basic validation that it's a valid golden dataset
                    self.assertIn("user_profile", dataset)
                    self.assertIn("expected_recommendations", dataset)
                    self.assertIn("validation_criteria", dataset)
                    
                except json.JSONDecodeError as e:
                    self.fail(f"Invalid JSON in {json_file}: {e}")
                except Exception as e:
                    self.fail(f"Error processing {json_file}: {e}")


if __name__ == '__main__':
    unittest.main()