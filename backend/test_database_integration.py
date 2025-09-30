import pytest
from httpx import AsyncClient, ASGITransport
import sys
import os
from unittest.mock import patch, AsyncMock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app
from backend import models

@pytest.mark.asyncio
async def test_get_recommendations_uses_database():
    # Arrange
    with patch('backend.models.CareerModel.find_all') as mock_find_all:
        mock_find_all.return_value.to_list = AsyncMock(return_value=[])
        
        user_profile = {
            "user_id": "test_user",
            "skills": [{"name": "Python", "level": "advanced"}],
            "interests": ["AI"],
            "salary_expectations": {"min": 100000, "max": 150000, "currency": "USD"}
        }

        # Act
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/recommendations", json={"user_profile": user_profile})

        # Assert
        assert response.status_code == 200
        mock_find_all.assert_called_once()