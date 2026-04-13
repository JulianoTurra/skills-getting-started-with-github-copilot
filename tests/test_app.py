import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (client is already set up)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister_participant():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act - sign up
    response_signup = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response_signup.status_code == 200
    assert f"Signed up {email}" in response_signup.json()["message"]
    # Act - duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response_dup.status_code == 400
    # Act - unregister
    response_del = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response_del.status_code == 200
    assert f"Removed {email}" in response_del.json()["message"]
    # Act - unregister again
    response_del2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response_del2.status_code == 404
