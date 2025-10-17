#!/usr/bin/env python3
"""
Test script to verify the Claude API migration is working properly.
"""
import asyncio
import sys
import os
sys.path.append('backend')

from backend.app.ai.ai_client import AIClient
from backend.app.core.config import get_settings

async def test_claude_client():
    """Test the Claude AI client with a sample user assessment."""
    
    settings = get_settings()
    print(f"Testing Claude AI client with API key: {settings.AI_API_KEY[:20]}...")
    
    # Initialize the AI client
    ai_client = AIClient(
        api_key=settings.AI_API_KEY,
        model_name="claude-3-sonnet-20240229"
    )
    
    # Sample user assessment for testing
    sample_assessment = {
        "technicalSkills": ["Python", "JavaScript", "SQL"],
        "softSkills": ["Communication", "Problem-solving", "Teamwork"],
        "experience": "3 years",
        "careerGoals": "Become a senior software engineer",
        "currentRole": "Junior Developer",
        "educationLevel": "Bachelor's in Computer Science",
        "salaryExpectations": "$80,000 - $100,000",
        "industries": ["Technology", "Finance"],
        "interests": ["Machine Learning", "Web Development"],
        "workingWithData": 4,
        "workingWithPeople": 3,
        "creativeTasks": 4
    }
    
    print("\n=== Testing get_recommendations ===")
    try:
        recommendations = await ai_client.get_recommendations(sample_assessment)
        print(f"✅ Successfully got {len(recommendations)} recommendations")
        
        if recommendations:
            print("\nFirst recommendation:")
            first_rec = recommendations[0]
            for key, value in first_rec.items():
                print(f"  {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")
        return False
    
    print("\n=== Testing tune_recommendations ===")
    try:
        tuned_recommendations = await ai_client.tune_recommendations(
            recommendations, 
            "I want more remote opportunities in data science"
        )
        print(f"✅ Successfully tuned recommendations, got {len(tuned_recommendations)} results")
        
    except Exception as e:
        print(f"❌ Error tuning recommendations: {e}")
        return False
    
    print("\n🎉 All tests passed! Claude migration is working correctly.")
    return True

if __name__ == "__main__":
    print("🔧 Testing Claude API Migration")
    print("=" * 50)
    
    # Run the async test
    success = asyncio.run(test_claude_client())
    
    if success:
        print("\n✅ Migration test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Migration test failed!")
        sys.exit(1)