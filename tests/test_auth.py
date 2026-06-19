from fastapi.testclient import TestClient


def test_register_and_login(client: TestClient) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": "demo@example.com", "full_name": "Demo User", "password": "StrongPass123!"},
    )
    assert register_response.status_code == 201
    assert register_response.json()["email"] == "demo@example.com"

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "demo@example.com", "password": "StrongPass123!"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
