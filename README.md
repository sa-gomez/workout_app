# Workout Tracker

A basic fitness tracker web app: log workouts and the sets/reps/weight for each exercise.

## Stack

- [uv](https://docs.astral.sh/uv/) for project/dependency management
- FastAPI + Jinja2 server-rendered templates
- SQLModel (SQLAlchemy) over SQLite

## Run

```bash
uv run uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000.

The SQLite database (`workout_tracker.db`) is created automatically on first run.
