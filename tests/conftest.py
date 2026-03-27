import pytest
from app import crud

@pytest.fixture(autouse=True)
def clear_db():
    crud.users_db.clear()
    crud.exercises_db.clear()
    crud.workouts_db.clear()
    crud.user_id_counter = 1
    crud.exercise_id_counter = 1
    crud.workout_id_counter = 1
    yield