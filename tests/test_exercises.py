from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_exercise():
    response = client.post("/exercises/", json={"name": "Push-up", "description": "Chest exercise"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Push-up"
    assert data["id"] == 1

def test_list_exercises():
    client.post("/exercises/", json={"name": "Squat"})
    response = client.get("/exercises/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Squat"