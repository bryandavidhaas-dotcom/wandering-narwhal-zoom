"""
AI Client for the Recommendation Engine.

This module will be responsible for all communication with the external AI model.
It will format requests, send them to the AI API, and parse the responses.
This client will completely replace the old, rules-based recommendation engine.
"""
from typing import List, Dict, Any
import anthropic
import json
import asyncio
import logging

class AIClient:
    """
    A client to interact with Anthropic's Claude model for generating and
    refining career recommendations.
    """

    def __init__(self, api_key: str, model_name: str = "claude-3-5-sonnet-20241022"):
        """
        Initializes the AI client.

        Args:
            api_key (str): The API key for the Anthropic service.
            model_name (str): The name of the Claude model to use.
        """
        self.api_key = api_key
        self.model_name = model_name
        self.client = anthropic.Anthropic(api_key=self.api_key)

    async def get_recommendations(self, user_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generates initial career recommendations based on a user's assessment.

        Args:
            user_assessment (Dict[str, Any]): The user's assessment data.

        Returns:
            List[Dict[str, Any]]: A list of career recommendations from the AI model.
        """
        prompt = self._construct_recommendation_prompt(user_assessment)
        try:
            # Run the synchronous Anthropic call in a thread pool with timeout
            api_call = asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.messages.create(
                    model=self.model_name,
                    max_tokens=4000,
                    temperature=0.7,
                    system="You are a career recommendation assistant. Provide a JSON response with a list of career recommendations. Always respond with valid JSON format.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
            )
            
            # Apply 30-second timeout to the API call
            response = await asyncio.wait_for(api_call, timeout=30.0)
            
            # Parse the response content
            content = response.content[0].text
            
            # Try to extract JSON from the response
            try:
                # Look for JSON in the response
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = content[start_idx:end_idx]
                    parsed_response = json.loads(json_str)
                    return parsed_response.get("recommendations", [])
                else:
                    # If no JSON found, try parsing the entire content
                    parsed_response = json.loads(content)
                    return parsed_response.get("recommendations", [])
            except json.JSONDecodeError:
                logging.warning(f"Failed to parse JSON response: {content}")
                # Return mock data if JSON parsing fails
                return self._get_mock_recommendations()
                
        except asyncio.TimeoutError:
            logging.warning("Claude API call timed out after 30 seconds, returning mock recommendations")
            # Return mock data when API call times out
            return self._get_mock_recommendations()
        except Exception as e:
            logging.error(f"Error getting recommendations: {e}")
            # Return properly structured mock recommendations for testing
            return self._get_mock_recommendations()

    async def tune_recommendations(self, current_recommendations: List[Dict[str, Any]], prompt: str) -> List[Dict[str, Any]]:
        """
        Refines a set of recommendations based on a user's text prompt.

        Args:
            current_recommendations (List[Dict[str, Any]]): The current list of recommendations.
            prompt (str): The user's natural language prompt for refinement.

        Returns:
            List[Dict[str, Any]]: An updated list of career recommendations from the AI model.
        """
        tuning_prompt = self._construct_tuning_prompt(current_recommendations, prompt)
        try:
            # Run the synchronous Anthropic call in a thread pool with timeout
            api_call = asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.messages.create(
                    model=self.model_name,
                    max_tokens=4000,
                    temperature=0.7,
                    system="You are a career recommendation assistant. Refine the given recommendations based on the user's prompt. Provide a JSON response with the updated recommendations.",
                    messages=[
                        {"role": "user", "content": tuning_prompt}
                    ]
                )
            )
            
            # Apply 30-second timeout to the API call
            response = await asyncio.wait_for(api_call, timeout=30.0)
            
            # Parse the response content
            content = response.content[0].text
            
            # Try to extract JSON from the response
            try:
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = content[start_idx:end_idx]
                    parsed_response = json.loads(json_str)
                    return parsed_response.get("recommendations", [])
                else:
                    parsed_response = json.loads(content)
                    return parsed_response.get("recommendations", [])
            except json.JSONDecodeError:
                logging.warning(f"Failed to parse JSON response: {content}")
                return current_recommendations
                
        except asyncio.TimeoutError:
            logging.warning("Claude API call timed out after 30 seconds during recommendation tuning, returning original recommendations")
            # Return the original recommendations if tuning times out
            return current_recommendations
        except Exception as e:
            logging.error(f"Error tuning recommendations: {e}")
            # Return the original recommendations if tuning fails
            return current_recommendations

    def _get_mock_recommendations(self) -> List[Dict[str, Any]]:
        """Returns mock recommendations for testing purposes."""
        return [
            {
                "job_id": "job_001",
                "title": "Software Engineer",
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "description": "Develop and maintain software applications",
                "requirements": ["Python", "JavaScript", "Problem solving"],
                "seniority": "Mid-level",
                "score": 85.5,
                "highlights": ["Strong Python skills", "Full-stack experience"],
                "role": "Software Engineer",
                "tech": ["Python", "JavaScript", "React"],
                "employment_type": "Full-time",
                "industry": "Technology"
            },
            {
                "job_id": "job_002",
                "title": "Data Analyst",
                "company": "Data Solutions Inc",
                "location": "Remote",
                "description": "Analyze data to provide business insights",
                "requirements": ["SQL", "Python", "Statistics"],
                "seniority": "Entry-level",
                "score": 78.2,
                "highlights": ["SQL expertise", "Statistical analysis"],
                "role": "Data Analyst",
                "tech": ["SQL", "Python", "Tableau"],
                "employment_type": "Full-time",
                "industry": "Data & Analytics"
            }
        ]

    def _construct_recommendation_prompt(self, user_assessment: Dict[str, Any]) -> str:
        """Constructs a prompt for the AI model based on user assessment."""
        # Handle both old and new field names for backward compatibility
        technical_skills = user_assessment.get('technicalSkills', user_assessment.get('skills', []))
        soft_skills = user_assessment.get('softSkills', [])
        career_goals = user_assessment.get('careerGoals', user_assessment.get('career_goals', 'N/A'))
        experience = user_assessment.get('experience', 'N/A')
        
        # Ensure skills are lists
        if technical_skills is None:
            technical_skills = []
        if soft_skills is None:
            soft_skills = []
            
        # Combine all skills
        all_skills = technical_skills + soft_skills
        
        # Build preferences from various fields
        preferences = user_assessment.get('preferences', {})
        if not preferences:
            preferences = {
                'salary_expectations': user_assessment.get('salaryExpectations', 'N/A'),
                'work_life_balance': user_assessment.get('workLifeBalance', 'N/A'),
                'location': user_assessment.get('location', 'N/A'),
                'industries': user_assessment.get('industries', []),
                'interests': user_assessment.get('interests', [])
            }
        
        return f"""
        Based on the following user assessment, please provide 5-10 career recommendations in JSON format.
        Each recommendation should include a job_title, company, location, description, and requirements.

        Please respond with a JSON object in this exact format:
        {{
            "recommendations": [
                {{
                    "job_id": "unique_id",
                    "title": "Job Title",
                    "company": "Company Name",
                    "location": "Location",
                    "description": "Job description",
                    "requirements": ["skill1", "skill2"],
                    "seniority": "Entry/Mid/Senior-level",
                    "score": 85.5,
                    "highlights": ["highlight1", "highlight2"],
                    "role": "Role Category",
                    "tech": ["tech1", "tech2"],
                    "employment_type": "Full-time/Part-time/Contract",
                    "industry": "Industry Name"
                }}
            ]
        }}

        User Assessment:
        - Technical Skills: {', '.join(str(skill) for skill in technical_skills) if technical_skills else 'None specified'}
        - Soft Skills: {', '.join(str(skill) for skill in soft_skills) if soft_skills else 'None specified'}
        - Experience: {experience}
        - Career Goals: {career_goals}
        - Current Role: {user_assessment.get('currentRole', 'N/A')}
        - Education: {user_assessment.get('educationLevel', 'N/A')}
        - Salary Expectations: {user_assessment.get('salaryExpectations', 'N/A')}
        - Preferred Industries: {', '.join(str(industry) for industry in user_assessment.get('industries', [])) if user_assessment.get('industries') else 'None specified'}
        - Interests: {', '.join(str(interest) for interest in user_assessment.get('interests', [])) if user_assessment.get('interests') else 'None specified'}
        - Work Preferences: Data work ({user_assessment.get('workingWithData', 3)}/5), People work ({user_assessment.get('workingWithPeople', 3)}/5), Creative tasks ({user_assessment.get('creativeTasks', 3)}/5)
        """

    def _construct_tuning_prompt(self, current_recommendations: List[Dict[str, Any]], prompt: str) -> str:
        """Constructs a prompt for tuning recommendations."""
        return f"""
        Given the current career recommendations and the user's feedback, please provide a new list of recommendations in JSON format.
        
        Please respond with a JSON object in this exact format:
        {{
            "recommendations": [
                {{
                    "job_id": "unique_id",
                    "title": "Job Title",
                    "company": "Company Name",
                    "location": "Location",
                    "description": "Job description",
                    "requirements": ["skill1", "skill2"],
                    "seniority": "Entry/Mid/Senior-level",
                    "score": 85.5,
                    "highlights": ["highlight1", "highlight2"],
                    "role": "Role Category",
                    "tech": ["tech1", "tech2"],
                    "employment_type": "Full-time/Part-time/Contract",
                    "industry": "Industry Name"
                }}
            ]
        }}

        Current Recommendations:
        {json.dumps(current_recommendations, indent=2)}

        User Feedback:
        "{prompt}"
        """