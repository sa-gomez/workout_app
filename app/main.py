from contextlib import asynccontextmanager
from datetime import date

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.db import get_session, init_db
from app.models import Exercise, ExerciseSet, Workout
from app.program import load_program


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Workout Tracker", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def index(request: Request, session: Session = Depends(get_session)):
    workouts = session.exec(select(Workout).order_by(Workout.date.desc())).all()
    return templates.TemplateResponse(
        request,
        "index.html",
        {"workouts": workouts, "today": date.today().isoformat()},
    )


@app.get("/program")
def program(request: Request):
    weeks = load_program()
    return templates.TemplateResponse(request, "program.html", {"weeks": weeks})


@app.post("/workouts")
def create_workout(
    workout_date: date = Form(default_factory=date.today),
    notes: str = Form(default=""),
    session: Session = Depends(get_session),
):
    workout = Workout(date=workout_date, notes=notes or None)
    session.add(workout)
    session.commit()
    session.refresh(workout)
    return RedirectResponse(f"/workouts/{workout.id}", status_code=303)


@app.get("/workouts/{workout_id}")
def workout_detail(
    workout_id: int, request: Request, session: Session = Depends(get_session)
):
    workout = session.get(Workout, workout_id)
    exercises = session.exec(select(Exercise).order_by(Exercise.name)).all()
    return templates.TemplateResponse(
        request,
        "workout_detail.html",
        {"workout": workout, "exercises": exercises},
    )


@app.post("/workouts/{workout_id}/sets")
def add_set(
    workout_id: int,
    exercise_name: str = Form(...),
    reps: int = Form(...),
    weight: float = Form(default=0),
    session: Session = Depends(get_session),
):
    exercise = session.exec(
        select(Exercise).where(Exercise.name == exercise_name.strip())
    ).first()
    if not exercise:
        exercise = Exercise(name=exercise_name.strip())
        session.add(exercise)
        session.commit()
        session.refresh(exercise)

    existing_sets = session.exec(
        select(ExerciseSet).where(
            ExerciseSet.workout_id == workout_id,
            ExerciseSet.exercise_id == exercise.id,
        )
    ).all()
    set_number = len(existing_sets) + 1

    exercise_set = ExerciseSet(
        workout_id=workout_id,
        exercise_id=exercise.id,
        reps=reps,
        weight=weight,
        set_number=set_number,
    )
    session.add(exercise_set)
    session.commit()
    return RedirectResponse(f"/workouts/{workout_id}", status_code=303)


@app.post("/workouts/{workout_id}/delete")
def delete_workout(workout_id: int, session: Session = Depends(get_session)):
    workout = session.get(Workout, workout_id)
    if workout:
        for exercise_set in workout.sets:
            session.delete(exercise_set)
        session.delete(workout)
        session.commit()
    return RedirectResponse("/", status_code=303)
