from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    expected_keys = {"Chess Club", "Programming Class", "Gym Class", "Soccer Team", "Swimming Club", "Art Studio", "Drama Club", "Math Olympiad", "Science Bowl"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert expected_keys.issubset(set(activities.keys()))


def test_signup_for_activity_returns_success_message():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400():
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    error = response.json()
    assert error["detail"] == "Student already signed up for this activity"


def test_remove_participant_returns_success_message():
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == f"Removed {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_remove_missing_participant_returns_404():
    # Arrange
    activity_name = "Gym Class"
    email = "missingstudent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    error = response.json()
    assert error["detail"] == "Participant not found"
