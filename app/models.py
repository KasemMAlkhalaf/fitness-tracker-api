from datetime import date
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class User:
    id: int
    username: str
    first_name: str
    last_name: str
    password_hash: str

@dataclass
class Exercise:
    id: int
    name: str
    description: Optional[str] = None

@dataclass
class WorkoutExercise:
    exercise_id: int
    sets: int
    reps: int
    weight: Optional[float] = None

@dataclass
class Workout:
    id: int
    user_id: int
    date: date
    exercises: List[WorkoutExercise] = field(default_factory=list)