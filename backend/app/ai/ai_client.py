"""
AI Client for the Recommendation Engine.

This module will be responsible for all communication with the external AI model.
It will format requests, send them to the AI API, and parse the responses.
This client will completely replace the old, rules-based recommendation engine.
"""
from typing import List, Dict, Any
import openai
import json
import httpx

class AIClient:
    """
    A client to interact with an external AI model for generating and
    refining career recommendations.
    """

    def __init__(self, api_key: str, model_name: str = "gpt-4"):
        """
        Initializes the AI client.

        Args:
            api_key (str): The API key for the AI service.
            model_name (str): The name of the model to use.
        """
        self.api_key = api_key
        self.model_name = model_name
        self.client = openai.OpenAI(
            api_key=self.api_key,
            http_client=httpx.Client()
        )

    def get_recommendations(self, user_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generates initial career recommendations based on a user's assessment.

        Args:
            user_assessment (Dict[str, Any]): The user's assessment data.

        Returns:
            List[Dict[str, Any]]: A list of career recommendations from the AI model.
        """
        prompt = self._construct_recommendation_prompt(user_assessment)
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a career recommendation assistant. Provide a JSON response with a list of career recommendations."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices.message.content).get("recommendations", [])
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []

    def tune_recommendations(self, current_recommendations: List[Dict[str, Any]], prompt: str) -> List[Dict[str, Any]]:
        """
        Refines a set of recommendations based on a user's text prompt.

        Args:
            current_recommendations (List[Dict[str, Any]]): The current list of recommendations.
            prompt (str): The user's natural language prompt for refinement.

        Returns:
            List[Dict[str, Any]]: An updated list of career recommendations from the AI model.
        """
        prompt = self._construct_tuning_prompt(current_recommendations, prompt)
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a career recommendation assistant. Refine the given recommendations based on the user's prompt. Provide a JSON response."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices.message.content).get("recommendations", [])
        except Exception as e:
            print(f"Error tuning recommendations: {e}")
            return []

    def _construct_recommendation_prompt(self, user_assessment: Dict[str, Any]) -> str:
        """Constructs a prompt for the AI model based on user assessment."""
        return f"""
        Based on the following user assessment, please provide 5-10 career recommendations in JSON format.
        Each recommendation should include a job_title, company, location, description, and requirements.

        User Assessment:
        - Skills: {', '.join(user_assessment.get('skills', []))}
        - Experience: {user_assessment.get('experience', 'N/A')}
        - Career Goals: {user_assessment.get('career_goals', 'N/A')}
        - Preferences: {user_assessment.get('preferences', {})}
        """

    def _construct_tuning_prompt(self, current_recommendations: List[Dict[str, Any]], prompt: str) -> str:
        """Constructs a prompt for tuning recommendations."""
        return f"""
        Given the current career recommendations and the user's feedback, please provide a new list of recommendations in JSON format.

        Current Recommendations:
        {json.dumps(current_recommendations, indent=2)}

        User Feedback:
        "{prompt}"
        """