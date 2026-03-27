# Fitness Tracker API

A RESTful API for a fitness tracker built with FastAPI. Supports user management, exercise library, workout logging, and statistics. Implements JWT authentication and includes OpenAPI documentation.

## Features
- User registration and login (JWT)
- Search users by login or by name/surname mask
- Manage exercises (create, list)
- Create workouts and add exercises to them
- Retrieve workout history and statistics for a date range
- In-memory storage (can be replaced with SQLite)
- Automatic OpenAPI docs at `/docs`

## Run Locally

1. Clone the repository: