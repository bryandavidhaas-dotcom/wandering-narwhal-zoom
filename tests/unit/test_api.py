import pytest
from fastapi.testclient import TestClient
from backend.simple_server import app, CAREER_DATA

client = TestClient(app)

def test_get_career_detail_success():
    """
    Test successful retrieval of a career from the /api/career/{career_type} endpoint.
    """
    # Select a career from the loaded data to test against
    assert isinstance(CAREER_DATA, list)
    assert len(CAREER_DATA) > 0
    career_to_test = CAREER_DATA[0]
    career_type = career_to_test["careerType"]

    response = client.get(f"/api/career/{career_type}")
    
    assert response.status_code == 200
    
    response_data = response.json()
    
    # Verify that the response data matches the test data
    assert response_data["title"] == career_to_test["title"]
    assert response_data["description"] == career_to_test["description"]
    assert response_data["careerType"] == career_to_test["careerType"]
    assert "dayInLife" in response_data

def test_get_career_detail_not_found():
    """
    Test the response for a career that does not exist.
    """
    non_existent_career_type = "non-existent-career"
    
    response = client.get(f"/api/career/{non_existent_career_type}")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Career not found"}

def test_get_career_detail_response_structure():
    """
    Test that the response structure for a valid career is correct.
    """
    # Select a career from the loaded data to test against
    assert isinstance(CAREER_DATA, list)
    assert len(CAREER_DATA) > 0
    career_to_test = CAREER_DATA[0]
    career_type = career_to_test["careerType"]

    response = client.get(f"/api/career/{career_type}")
    
    assert response.status_code == 200
    
    response_data = response.json()
    
    # Check for the presence of key fields
    assert "title" in response_data
    assert "description" in response_data
    assert "dayInLife" in response_data
    assert "requiredTechnicalSkills" in response_data
    assert "requiredSoftSkills" in response_data
    assert "salaryRange" in response_data
    assert "experienceLevel" in response_data