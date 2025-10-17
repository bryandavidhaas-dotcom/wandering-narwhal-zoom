#!/usr/bin/env python3
"""
Test script to verify AI client functionality after timeout fixes.
This script tests both timeout handling and normal operation.
"""

import asyncio
import sys
import os
import time
import json
from unittest.mock import Mock, patch

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.ai.ai_client import AIClient

async def test_ai_client_functionality():
    """Test that the AI client works correctly with timeout fixes."""
    print("Testing AI Client functionality after timeout fixes...")
    
    # Create AI client with dummy API key for testing
    ai_client = AIClient(api_key="test-key")
    
    # Mock user assessment data
    user_assessment = {
        'technicalSkills': ['Python', 'JavaScript', 'React'],
        'softSkills': ['Communication', 'Problem Solving', 'Leadership'],
        'experience': '3 years',
        'careerGoals': 'Full Stack Development',
        'currentRole': 'Software Developer',
        'educationLevel': 'Bachelor\'s Degree in Computer Science',
        'salaryExpectations': '$80,000',
        'industries': ['Technology', 'Fintech'],
        'interests': ['Web Development', 'Machine Learning'],
        'workingWithData': 4,
        'workingWithPeople': 3,
        'creativeTasks': 4
    }
    
    # Test 1: Normal operation with successful API response
    print("\n1. Testing normal operation...")
    
    mock_response = Mock()
    mock_response.content = [Mock()]
    mock_response.content[0].text = json.dumps({
        "recommendations": [
            {
                "job_id": "job_001",
                "title": "Full Stack Developer",
                "company": "Tech Innovations Inc",
                "location": "San Francisco, CA",
                "description": "Develop and maintain web applications using modern technologies",
                "requirements": ["Python", "JavaScript", "React", "Node.js"],
                "seniority": "Mid-level",
                "score": 92.5,
                "highlights": ["Strong React skills", "Full-stack experience", "Problem solving"],
                "role": "Full Stack Developer",
                "tech": ["Python", "JavaScript", "React", "Node.js"],
                "employment_type": "Full-time",
                "industry": "Technology"
            },
            {
                "job_id": "job_002",
                "title": "Frontend Developer",
                "company": "Digital Solutions LLC",
                "location": "Remote",
                "description": "Create responsive and interactive user interfaces",
                "requirements": ["JavaScript", "React", "CSS", "HTML"],
                "seniority": "Mid-level",
                "score": 88.0,
                "highlights": ["React expertise", "UI/UX focus"],
                "role": "Frontend Developer",
                "tech": ["JavaScript", "React", "CSS", "HTML"],
                "employment_type": "Full-time",
                "industry": "Technology"
            }
        ]
    })
    
    with patch.object(ai_client.client.messages, 'create', return_value=mock_response):
        start_time = time.time()
        recommendations = await ai_client.get_recommendations(user_assessment)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        print(f"   - API call completed in {elapsed_time:.3f} seconds")
        
        if recommendations and len(recommendations) == 2:
            print("   ✓ Correct number of recommendations returned")
            print(f"   - First recommendation: {recommendations[0]['title']}")
            print(f"   - Second recommendation: {recommendations[1]['title']}")
            
            # Verify structure
            required_fields = ['job_id', 'title', 'company', 'location', 'description', 
                             'requirements', 'seniority', 'score', 'highlights', 'role', 
                             'tech', 'employment_type', 'industry']
            
            all_fields_present = all(field in recommendations[0] for field in required_fields)
            if all_fields_present:
                print("   ✓ All required fields present in recommendations")
            else:
                print("   ✗ Missing required fields in recommendations")
        else:
            print("   ✗ Incorrect number of recommendations returned")
    
    # Test 2: Test recommendation tuning
    print("\n2. Testing recommendation tuning...")
    
    current_recommendations = [
        {
            "job_id": "job_001",
            "title": "Junior Developer",
            "company": "StartupCorp",
            "location": "Austin, TX",
            "description": "Entry-level development position",
            "requirements": ["Python", "Git"],
            "seniority": "Entry-level",
            "score": 75.0,
            "highlights": ["Good Python skills"],
            "role": "Software Developer",
            "tech": ["Python"],
            "employment_type": "Full-time",
            "industry": "Technology"
        }
    ]
    
    tuned_mock_response = Mock()
    tuned_mock_response.content = [Mock()]
    tuned_mock_response.content[0].text = json.dumps({
        "recommendations": [
            {
                "job_id": "job_003",
                "title": "Senior Python Developer",
                "company": "Enterprise Solutions",
                "location": "New York, NY",
                "description": "Senior-level Python development with leadership responsibilities",
                "requirements": ["Python", "Django", "Leadership", "Architecture"],
                "seniority": "Senior-level",
                "score": 95.0,
                "highlights": ["Senior Python expertise", "Leadership experience"],
                "role": "Senior Software Developer",
                "tech": ["Python", "Django", "PostgreSQL"],
                "employment_type": "Full-time",
                "industry": "Technology"
            }
        ]
    })
    
    with patch.object(ai_client.client.messages, 'create', return_value=tuned_mock_response):
        tuned_recommendations = await ai_client.tune_recommendations(
            current_recommendations, 
            "I want more senior-level positions with higher salary"
        )
        
        if tuned_recommendations and len(tuned_recommendations) == 1:
            print("   ✓ Recommendation tuning working correctly")
            print(f"   - Tuned recommendation: {tuned_recommendations[0]['title']}")
            print(f"   - Seniority level: {tuned_recommendations[0]['seniority']}")
        else:
            print("   ✗ Recommendation tuning failed")
    
    # Test 3: Test timeout handling (already tested in previous script, but verify it still works)
    print("\n3. Testing timeout handling...")
    
    def mock_hanging_api_call(*args, **kwargs):
        """Mock API call that hangs."""
        time.sleep(35)  # Sleep longer than timeout
        return Mock()
    
    with patch.object(ai_client.client.messages, 'create', side_effect=mock_hanging_api_call):
        start_time = time.time()
        timeout_recommendations = await ai_client.get_recommendations(user_assessment)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        print(f"   - Timeout test completed in {elapsed_time:.2f} seconds")
        
        if elapsed_time < 35 and timeout_recommendations:
            print("   ✓ Timeout handling working correctly")
            print(f"   - Returned {len(timeout_recommendations)} mock recommendations")
        else:
            print("   ✗ Timeout handling failed")
    
    # Test 4: Test JSON parsing error handling
    print("\n4. Testing JSON parsing error handling...")
    
    invalid_json_response = Mock()
    invalid_json_response.content = [Mock()]
    invalid_json_response.content[0].text = "This is not valid JSON response from the API"
    
    with patch.object(ai_client.client.messages, 'create', return_value=invalid_json_response):
        error_recommendations = await ai_client.get_recommendations(user_assessment)
        
        if error_recommendations and len(error_recommendations) > 0:
            print("   ✓ JSON parsing error handled correctly")
            print(f"   - Returned {len(error_recommendations)} mock recommendations")
        else:
            print("   ✗ JSON parsing error handling failed")
    
    print("\n✓ All AI Client functionality tests completed!")

if __name__ == "__main__":
    asyncio.run(test_ai_client_functionality())