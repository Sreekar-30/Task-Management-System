from fastapi.testclient import TestClient


def auth_headers(client: TestClient) -> dict[str, str]:
    client.post(
        "/api/v1/auth/register",
        json={"email": "spender@example.com", "full_name": "Spender User", "password": "StrongPass123!"},
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "spender@example.com", "password": "StrongPass123!"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_expense_crud_and_filters(client: TestClient) -> None:
    headers = auth_headers(client)
    category = client.post("/api/v1/categories", json={"name": "Groceries"}, headers=headers).json()

    create_response = client.post(
        "/api/v1/expenses",
        json={
            "title": "Weekly groceries",
            "amount": "82.45",
            "expense_date": "2026-06-19",
            "category_id": category["id"],
            "payment_method_id": 1,
            "description": "Pantry refill",
        },
        headers=headers,
    )
    assert create_response.status_code == 201
    expense_id = create_response.json()["id"]

    list_response = client.get("/api/v1/expenses?search=groceries&min_amount=10", headers=headers)
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    update_response = client.put(f"/api/v1/expenses/{expense_id}", json={"amount": "90.00"}, headers=headers)
    assert update_response.status_code == 200
    assert update_response.json()["amount"] == "90.00"

    delete_response = client.delete(f"/api/v1/expenses/{expense_id}", headers=headers)
    assert delete_response.status_code == 204
