from typing import List, Optional, Dict
from datetime import date
from .models import User, Exercise, Workout, WorkoutExercise

# In-memory storage
users_db: Dict[int, User] = {}
exercises_db: Dict[int, Exercise] = {}
workouts_db: Dict[int, Workout] = {}

# ID counters
user_id_counter = 1
exercise_id_counter = 1
workout_id_counter = 1

# User operations
def create_user(username: str, first_name: str, last_name: str, password_hash: str) -> User:
    global user_id_counter
    user = User(id=user_id_counter, username=username, first_name=first_name, last_name=last_name, password_hash=password_hash)
    users_db[user.id] = user
    user_id_counter += 1
    return user

def get_user_by_username(username: str) -> Optional[User]:
    for user in users_db.values():
        if user.username == username:
            return user
    return None

def get_user_by_id(user_id: int) -> Optional[User]:
    return users_db.get(user_id)

def search_users_by_name(first_name_mask: str, last_name_mask: str) -> List[User]:
    result = []
    for user in users_db.values():
        if (first_name_mask.lower() in user.first_name.lower() if first_name_mask else True) and \
           (last_name_mask.lower() in user.last_name.lower() if last_name_mask else True):
            result.append(user)
    return result

# Exercise operations
def create_exercise(name: str, description: Optional[str] = None) -> Exercise:
    global exercise_id_counter
    exercise = Exercise(id=exercise_id_counter, name=name, description=description)
    exercises_db[exercise.id] = exercise
    exercise_id_counter += 1
    return exercise

def get_exercises() -> List[Exercise]:
    return list(exercises_db.values())

def get_exercise_by_id(exercise_id: int) -> Optional[Exercise]:
    return exercises_db.get(exercise_id)

# Workout operations
def create_workout(user_id: int, workout_date: date) -> Workout:
    global workout_id_counter
    workout = Workout(id=workout_id_counter, user_id=user_id, date=workout_date, exercises=[])
    workouts_db[workout.id] = workout
    workout_id_counter += 1
    return workout

def get_workout_by_id(workout_id: int) -> Optional[Workout]:
    return workouts_db.get(workout_id)

def get_workouts_by_user(user_id: int) -> List[Workout]:
    return [w for w in workouts_db.values() if w.user_id == user_id]

def add_exercise_to_workout(workout_id: int, exercise_id: int, sets: int, reps: int, weight: Optional[float]) -> Optional[Workout]:
    workout = workouts_db.get(workout_id)
    if not workout:
        return None
    exercise = exercises_db.get(exercise_id)
    if not exercise:
        return None
    workout_exercise = WorkoutExercise(exercise_id=exercise_id, sets=sets, reps=reps, weight=weight)
    workout.exercises.append(workout_exercise)
    return workout

def get_workout_stats(user_id: int, start_date: date, end_date: date):
    workouts = get_workouts_by_user(user_id)
    filtered = [w for w in workouts if start_date <= w.date <= end_date]
    total_workouts = len(filtered)
    total_exercises = sum(len(w.exercises) for w in filtered)
    total_volume = 0.0
    for w in filtered:
        for we in w.exercises:
            if we.weight:
                total_volume += we.weight * we.reps * we.sets
    return {
        "total_workouts": total_workouts,
        "total_exercises": total_exercises,
        "total_volume": total_volume,
        "start_date": start_date,
        "end_date": end_date
    }