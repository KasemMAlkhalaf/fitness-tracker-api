from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from datetime import date
from .. import crud, schemas, auth

router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.post("/", response_model=schemas.WorkoutResponse, status_code=status.HTTP_201_CREATED)
def create_workout(workout_data: schemas.WorkoutCreate, current_user=Depends(auth.get_current_user)):
    workout = crud.create_workout(current_user.id, workout_data.date)
    return schemas.WorkoutResponse(id=workout.id, user_id=workout.user_id, date=workout.date, exercises=[])

@router.post("/{workout_id}/exercises", response_model=schemas.WorkoutResponse)
def add_exercise_to_workout(
    workout_id: int,
    exercise_data: schemas.WorkoutExerciseCreate,
    current_user=Depends(auth.get_current_user)
):
    workout = crud.get_workout_by_id(workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    if workout.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this workout")
    if not crud.get_exercise_by_id(exercise_data.exercise_id):
        raise HTTPException(status_code=404, detail="Exercise not found")
    updated = crud.add_exercise_to_workout(
        workout_id, exercise_data.exercise_id, exercise_data.sets, exercise_data.reps, exercise_data.weight
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Workout not found")
    # Build response with exercise names
    exercises_resp = []
    for we in updated.exercises:
        ex = crud.get_exercise_by_id(we.exercise_id)
        exercises_resp.append(schemas.WorkoutExerciseResponse(
            exercise_id=we.exercise_id,
            exercise_name=ex.name if ex else None,
            sets=we.sets,
            reps=we.reps,
            weight=we.weight
        ))
    return schemas.WorkoutResponse(id=updated.id, user_id=updated.user_id, date=updated.date, exercises=exercises_resp)

@router.get("/history", response_model=List[schemas.WorkoutResponse])
def get_workout_history(current_user=Depends(auth.get_current_user)):
    workouts = crud.get_workouts_by_user(current_user.id)
    result = []
    for w in workouts:
        exercises_resp = []
        for we in w.exercises:
            ex = crud.get_exercise_by_id(we.exercise_id)
            exercises_resp.append(schemas.WorkoutExerciseResponse(
                exercise_id=we.exercise_id,
                exercise_name=ex.name if ex else None,
                sets=we.sets,
                reps=we.reps,
                weight=we.weight
            ))
        result.append(schemas.WorkoutResponse(id=w.id, user_id=w.user_id, date=w.date, exercises=exercises_resp))
    return result

@router.get("/stats", response_model=schemas.StatsResponse)
def get_workout_stats(
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_user=Depends(auth.get_current_user)
):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")
    stats = crud.get_workout_stats(current_user.id, start_date, end_date)
    return stats