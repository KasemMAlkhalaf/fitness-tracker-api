from fastapi import FastAPI
from .routers import auth, users, exercises, workouts

app = FastAPI(title="Fitness Tracker API", version="1.0.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(exercises.router)
app.include_router(workouts.router)

@app.get("/")
def root():
    return {"message": "Fitness Tracker API"}