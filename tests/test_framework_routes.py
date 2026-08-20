def test_docs_route_is_available(client):
    # Arrange
    route = "/docs"

    # Act
    response = client.get(route)

    # Assert
    assert response.status_code == 200


def test_openapi_route_contains_expected_paths(client):
    # Arrange
    expected_paths = {
        "/",
        "/activities",
        "/activities/{activity_name}/signup",
        "/activities/{activity_name}/participants",
    }

    # Act
    response = client.get("/openapi.json")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_paths.issubset(set(payload["paths"].keys()))


def test_static_index_route_is_available(client):
    # Arrange
    route = "/static/index.html"

    # Act
    response = client.get(route)

    # Assert
    assert response.status_code == 200
