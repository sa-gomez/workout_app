import csv
import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_PATH = DATA_DIR / "ppl_phase1.csv"
VIDEO_LINKS_PATH = DATA_DIR / "exercise_video_links.json"


@dataclass
class ProgramExercise:
    name: str
    warmup_sets: str
    working_sets: str
    reps: str
    rpe: str
    rest: str
    sub1: str
    sub2: str
    notes: str
    video_url: str | None = None


@dataclass
class ProgramDay:
    label: str
    exercises: list[ProgramExercise] = field(default_factory=list)


@dataclass
class ProgramWeek:
    label: str
    days: list[ProgramDay] = field(default_factory=list)


@lru_cache
def load_video_links() -> dict[str, str]:
    with open(VIDEO_LINKS_PATH, encoding="utf-8") as f:
        return json.load(f)


@lru_cache
def load_program() -> list[ProgramWeek]:
    video_links = load_video_links()

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    weeks: list[ProgramWeek] = []
    current_week: ProgramWeek | None = None
    current_day: ProgramDay | None = None

    for row in rows:
        row = row + [""] * (11 - len(row))
        label, name = row[0].strip(), row[1].strip()

        if label.startswith("Week ") and name == "Exercise":
            current_week = ProgramWeek(label=label)
            weeks.append(current_week)
            current_day = None
            continue

        if current_week is None:
            continue

        if not name:
            current_day = None
            continue

        if label:
            current_day = ProgramDay(label=label)
            current_week.days.append(current_day)

        if current_day is None:
            continue

        current_day.exercises.append(
            ProgramExercise(
                name=name,
                warmup_sets=row[2].strip(),
                working_sets=row[3].strip(),
                reps=row[4].strip(),
                rpe=row[6].strip(),
                rest=row[7].strip(),
                sub1=row[8].strip(),
                sub2=row[9].strip(),
                notes=row[10].strip(),
                video_url=video_links.get(name),
            )
        )

    return weeks
