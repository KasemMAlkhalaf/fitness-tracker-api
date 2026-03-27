from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_user_by_login():
    client.post("/auth/register", json={"username": "searchme", "first_name": "Jane", "last_name": "Smith", "password": "pass"})
    response = client.get("/users/login/searchme")
    assert response.status_code == 200
    assert response.json()["username"] == "searchme"

def test_search_user_by_login_not_found():
    response = client.get("/users/login/nonexistent")
    assert response.status_code == 404

def test_search_users_by_name_mask():
    client.post("/auth/register", json={"username": "u1", "first_name": "Alice", "last_name": "Wonder", "password": "p"})
    client.post("/auth/register", json={"username": "u2", "first_name": "Bob", "last_name": "Builder", "password": "p"})
    response = client.get("/users/search?first_name=ali&last_name=won")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "u1"