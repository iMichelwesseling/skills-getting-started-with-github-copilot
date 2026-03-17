import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert pattern is used in all tests

def test_get_activities():
    # Arrange: (nothing to arrange for this test)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json().get("message", "")
    # Clean up: remove test user if needed
    data = client.get("/activities").json()
    if email in data[activity]["participants"]:
        data[activity]["participants"].remove(email)

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    # Ensure user is signed up first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")
    # Clean up
    data = client.get("/activities").json()
    if email in data[activity]["participants"]:
        data[activity]["participants"].remove(email)

def test_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "testuser3@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
