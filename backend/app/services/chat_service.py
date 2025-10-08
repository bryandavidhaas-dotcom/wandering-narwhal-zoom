from app.models.assessment import UserAssessment
from typing import Dict, Any

def get_ai_chat_response(message: str, assessment_data: Dict[str, Any]) -> str:
    """
    Generates an AI response to a user's chat message based on their assessment data.
    """
    prompt = f"""
    The user has completed a career assessment and has the following profile:
    - Skills: {assessment_data.get("skills", "N/A")}
    - Interests: {assessment_data.get("interests", "N/A")}
    - Career Recommendations: {assessment_data.get("recommendations", "N/A")}

    The user's message is: "{message}"

    Based on their assessment results, provide a helpful and encouraging response.
    If the user asks about a specific career, provide some information about it.
    If the user's question is unclear, ask for clarification.
    """

    # You can replace this with a call to your preferred AI service (e.g., OpenAI, Cohere)
    # For now, we'll return a mock response.
    # return get_completion(prompt)
    
    return "This is a mock response. In a real application, I would provide a more detailed answer based on your assessment."