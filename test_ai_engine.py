import unittest
import unittest
from pydantic import BaseModel
from typing import List, Dict, Any
from backend.recommendation_engine.enhanced_engine import EnhancedRecommendationEngine
from backend.recommendation_engine.mock_data import create_mock_user_profile, create_mock_careers

class CareerRecommendation(BaseModel):
    user_id: str
    career_id: str
    career: Any
    score: Any
    category: Any
    reasons: List[str]
    confidence: float

class TestAIEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EnhancedRecommendationEngine()

    def test_get_recommendations(self):
        """
        Tests that the enhanced recommendation engine can generate recommendations.
        """
        mock_user_profile = create_mock_user_profile()
        mock_careers = create_mock_careers()

        recommendations = self.engine.get_recommendations(mock_user_profile, mock_careers)
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0, "Should generate at least one recommendation")
        
        # Validate the structure of the recommendations
        for rec in recommendations:
            CareerRecommendation.model_validate(rec)

if __name__ == '__main__':
    unittest.main()