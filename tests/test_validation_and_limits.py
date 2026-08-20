from src.app import activities


def test_signup_rejects_empty_email_with_422(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": ""})

    # Assert
    assert response.status_code == 422


def test_unregister_rejects_invalid_email_with_422(client):
    # Arrange
    activity_name = "Chess Club"
    invalid_email = "not-an-email"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": invalid_email},
    )

    # Assert
    assert response.status_code == 422


def test_signup_rejects_when_participant_limit_is_reached(client):
    # Arrange
    activity_name = "Chess Club"
    activity = activities[activity_name]
    activity["max_participants"] = len(activity["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "limit.test@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
