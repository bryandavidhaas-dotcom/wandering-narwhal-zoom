#!/usr/bin/env python3
"""
Test script to verify Claude API timeout implementation.
This script tests that the AI client properly handles timeouts and returns mock data.
"""

import asyncio
import sys
import os
import time
from unittest.mock import Mock, patch

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.ai.ai_client import AIClient

async def test_timeout_handling():
    """Test that the AI client properly handles timeouts."""
    print("Testing Claude API timeout handling...")
    
    # Create AI client with dummy API key for testing
    ai_client = AIClient(api_key="test-key")
    
    # Mock user assessment data
    user_assessment = {
        'technicalSkills': ['Python', 'JavaScript'],
        'softSkills': ['Communication', 'Problem Solving'],
        'experience': '2 years',
        'careerGoals': 'Software Development',
        'currentRole': 'Junior Developer',
        'educationLevel': 'Bachelor\'s Degree',
        'salaryExpectations': '$70,000',
        'industries': ['Technology'],
        'interests': ['Web Development', 'AI']
    }
    
    # Test 1: Simulate timeout by mocking the API call to hang
    print("\n1. Testing timeout scenario...")
    
    def mock_hanging_api_call(*args, **kwargs):
        """Mock API call that hangs indefinitely."""
        time.sleep(35)  # Sleep longer than our 30-second timeout
        return Mock()
    
    with patch.object(ai_client.client.messages, 'create', side_effect=mock_hanging_api_call):
        start_time = time.time()
        recommendations = await ai_client.get_recommendations(user_assessment)
        end_time = time.time()
        
        # Verify timeout occurred within reasonable time (should be ~30 seconds)
        elapsed_time = end_time - start_time
        print(f"   - API call completed in {elapsed_time:.2f} seconds")
        
        if elapsed_time < 35:  # Should timeout before 35 seconds
            print("   ✓ Timeout handling working correctly")
        else:
            print("   ✗ Timeout not working - call took too long")
            
        # Verify mock recommendations were returned
        if recommendations and len(recommendations) > 0:
            print("   ✓ Mock recommendations returned on timeout")
            print(f"   - Returned {len(recommendations)} recommendations")
        else:
            print("   ✗ No recommendations returned on timeout")
    
    # Test 2: Test normal operation (mock successful response)
    print("\n2. Testing normal operation...")
    
    mock_response = Mock()
    mock_response.content = [Mock()]
    mock_response.content[0].text = '''
    {
        "recommendations": [
            {
                "job_id": "test_001",
                "title": "Test Engineer",
                "company": "Test Corp",
                "location": "Test City",
                "description": "Test job description",
                "requirements": ["Testing", "Python"],
                "seniority": "Mid-level",
                "score": 90.0,
                "highlights": ["Test highlight"],
                "role": "Test Role",
                "tech": ["Python", "Testing"],
                "employment_type": "Full-time",
                "industry": "Testing"
            }
        ]
    }
    '''
    
    with patch.object(ai_client.client.messages, 'create', return_value=mock_response):
        start_time = time.time()
        recommendations = await ai_client.get_recommendations(user_assessment)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        print(f"   - API call completed in {elapsed_time:.2f} seconds")
        
        if elapsed_time < 5:  # Should be fast with mocked response
            print("   ✓ Normal operation working correctly")
        else:
            print("   ✗ Normal operation too slow")
            
        # Verify actual recommendations were returned
        if recommendations and len(recommendations) > 0 and recommendations[0].get('title') == 'Test Engineer':
            print("   ✓ Actual recommendations returned in normal operation")
        else:
            print("   ✗ Incorrect recommendations in normal operation")
    
    # Test 3: Test tune_recommendations timeout
    print("\n3. Testing tune_recommendations timeout...")
    
    current_recommendations = [
        {
            "job_id": "current_001",
            "title": "Current Job",
            "company": "Current Corp",
            "location": "Current City",
            "description": "Current description",
            "requirements": ["Current skill"],
            "seniority": "Mid-level",
            "score": 80.0,
            "highlights": ["Current highlight"],
            "role": "Current Role",
            "tech": ["Current Tech"],
            "employment_type": "Full-time",
            "industry": "Current Industry"
        }
    ]
    
    with patch.object(ai_client.client.messages, 'create', side_effect=mock_hanging_api_call):
        start_time = time.time()
        tuned_recommendations = await ai_client.tune_recommendations(current_recommendations, "Make it more senior level")
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        print(f"   - Tune API call completed in {elapsed_time:.2f} seconds")
        
        if elapsed_time < 35:  # Should timeout before 35 seconds
            print("   ✓ Tune timeout handling working correctly")
        else:
            print("   ✗ Tune timeout not working - call took too long")
            
        # Verify original recommendations were returned on timeout
        if tuned_recommendations == current_recommendations:
            print("   ✓ Original recommendations returned on tune timeout")
        else:
            print("   ✗ Incorrect recommendations returned on tune timeout")
    
    print("\n✓ All timeout tests completed!")

if __name__ == "__main__":
    asyncio.run(test_timeout_handling())