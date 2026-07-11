import datetime as dt

from sqlmodel import Field, Relationship, SQLModel


class Exercise(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    sets: list["ExerciseSet"] = Relationship(back_populates="exercise")


class Workout(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: dt.date = Field(default_factory=dt.date.today, index=True)
    day_type: str | None = None
    notes: str | None = None
    created_at: dt.datetime = Field(default_factory=dt.datetime.utcnow)

    sets: list["ExerciseSet"] = Relationship(back_populates="workout")


class ExerciseSet(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    workout_id: int = Field(foreign_key="workout.id")
    exercise_id: int = Field(foreign_key="exercise.id")
    reps: int
    weight: float = 0
    set_number: int = 1

    workout: Workout = Relationship(back_populates="sets")
    exercise: Exercise = Relationship(back_populates="sets")
