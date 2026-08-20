from src.app import activities


def test_unregister_removes_participant_for_valid_request(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_student_not_in_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "absent.student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_returns_422_when_email_is_missing(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants")

    # Assert
    assert response.status_code == 422


def test_unregister_returns_422_when_email_is_invalid(client):
    # Arrange
    activity_name = "Chess Club"
    invalid_email = "invalid-email"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": invalid_email},
    )

    # Assert
    assert response.status_code == 422


def test_unregister_returns_404_when_repeated_after_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]
    first_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    assert first_response.status_code == 200

    # Act
    second_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert second_response.status_code == 404
    assert second_response.json()["detail"] == "Student not signed up for this activity"
