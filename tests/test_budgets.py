from fastapi.testclient import TestClient

from tests.test_expenses import auth_headers


def test_budget_status(client: TestClient) -> None:
    headers = auth_headers(client)
    response = client.post(
        "/api/v1/budgets",
        json={"month": 6, "year": 2026, "amount": "1000.00", "alert_threshold_percent": "80.00"},
        headers=headers,
    )
    assert response.status_code == 201

    status_response = client.get("/api/v1/budgets/status/2026/6", headers=headers)
    assert status_response.status_code == 200
    assert status_response.json()["remaining_amount"] == "1000.00"
