import requests
import json

# Define the API endpoint
url = "http://127.0.0.1:8000/api/recommendations"

# Sample user profile for the POST request
user_profile = {
    "username": "test_user",
    "preferences": {
        "industry": "Tech",
        "interests": ["Software Development", "Data Science"]
    }
}

# Make the POST request
response = requests.post(url, json=user_profile)

# Assert that the request was successful
assert response.status_code == 200, f"Request failed with status code {response.status_code}"

# Parse the JSON response
recommendations = response.json()

# Iterate through recommendations and assert kebab-case format
for rec in recommendations:
    career_type = rec.get("careerType", "")
    assert all(c.islower() or c.isdigit() or c == '-' for c in career_type), f"Career type '{career_type}' is not in kebab-case."
    assert ' ' not in career_type, f"Career type '{career_type}' contains spaces."

# If all assertions pass, print a success message
print("SUCCESS: Career titles are correctly normalized to kebab-case.")