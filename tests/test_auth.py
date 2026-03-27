from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_success():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "first_name": "John",
        "last_name": "Doe",
        "password": "secret"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_register_duplicate():
    client.post("/auth/register", json={"username": "dup", "first_name": "A", "last_name": "B", "password": "pwd"})
    response = client.post("/auth/register", json={"username": "dup", "first_name": "A", "last_name": "B", "password": "pwd"})
    assert response.status_code == 409

def test_login_success():
    client.post("/auth/register", json={"username": "loginuser", "first_name": "A", "last_name": "B", "password": "pass"})
    response = client.post("/auth/login", data={"username": "loginuser", "password": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    client.post("/auth/register", json={"username": "badpass", "first_name": "A", "last_name": "B", "password": "correct"})
    response = client.post("/auth/login", data={"username": "badpass", "password": "wrong"})
    assert response.status_code == 401