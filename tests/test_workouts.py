from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token():
    client.post("/auth/register", json={"username": "workoutuser", "first_name": "Test", "last_name": "User", "password": "pass"})
    res = client.post("/auth/login", data={"username": "workoutuser", "password": "pass"})
    return res.json()["access_token"]

def test_create_workout():
    token = get_token()
    response = client.post("/workouts/", json={"date": "2025-03-27"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["date"] == "2025-03-27"

def test_add_exercise_to_workout():
    token = get_token()
    # create exercise
    ex_resp = client.post("/exercises/", json={"name": "Bench Press"})
    ex_id = ex_resp.json()["id"]
    # create workout
    w_resp = client.post("/workouts/", json={"date": "2025-03-27"}, headers={"Authorization": f"Bearer {token}"})
    w_id = w_resp.json()["id"]
    # add exercise
    response = client.post(f"/workouts/{w_id}/exercises", json={"exercise_id": ex_id, "sets": 3, "reps": 10, "weight": 60.0},
                           headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["exercises"]) == 1
    assert data["exercises"][0]["exercise_name"] == "Bench Press"

def test_get_workout_history():
    token = get_token()
    # create workout
    client.post("/workouts/", json={"date": "2025-03-27"}, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/workouts/history", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["date"] == "2025-03-27"

def test_get_workout_stats():
    token = get_token()
    # create workout with exercise
    ex = client.post("/exercises/", json={"name": "Deadlift"}).json()
    w = client.post("/workouts/", json={"date": "2025-03-27"}, headers={"Authorization": f"Bearer {token}"}).json()
    client.post(f"/workouts/{w['id']}/exercises", json={"exercise_id": ex["id"], "sets": 5, "reps": 5, "weight": 100.0},
                headers={"Authorization": f"Bearer {token}"})
    response = client.get("/workouts/stats?start_date=2025-03-01&end_date=2025-03-31",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["total_workouts"] == 1
    assert data["total_exercises"] == 1
    assert data["total_volume"] == 100.0 * 5 * 5  # 2500

def test_stats_date_range_invalid():
    token = get_token()
    response = client.get("/workouts/stats?start_date=2025-03-31&end_date=2025-03-01",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400