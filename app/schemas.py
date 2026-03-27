from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

# User schemas
class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str

# Exercise schemas
class ExerciseCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ExerciseResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# Workout schemas
class WorkoutCreate(BaseModel):
    date: date

class WorkoutExerciseCreate(BaseModel):
    exercise_id: int
    sets: int = Field(..., ge=1)
    reps: int = Field(..., ge=1)
    weight: Optional[float] = Field(None, ge=0)

class WorkoutExerciseResponse(BaseModel):
    exercise_id: int
    exercise_name: Optional[str] = None
    sets: int
    reps: int
    weight: Optional[float] = None

class WorkoutResponse(BaseModel):
    id: int
    user_id: int
    date: date
    exercises: List[WorkoutExerciseResponse]

# Stats
class StatsResponse(BaseModel):
    total_workouts: int
    total_exercises: int
    total_volume: float
    start_date: date
    end_date: date

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str