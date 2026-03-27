from fastapi import APIRouter, status
from typing import List
from .. import crud, schemas

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.post("/", response_model=schemas.ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise_data: schemas.ExerciseCreate):
    return crud.create_exercise(exercise_data.name, exercise_data.description)

@router.get("/", response_model=List[schemas.ExerciseResponse])
def list_exercises():
    return crud.get_exercises()