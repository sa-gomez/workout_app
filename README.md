# Workout Tracker

A basic fitness tracker web app: log workouts and the sets/reps/weight for each exercise,
plus a reference tab for a structured training program.

## Stack

- [uv](https://docs.astral.sh/uv/) for project/dependency management
- FastAPI + Jinja2 server-rendered templates
- SQLModel (SQLAlchemy) over SQLite
- PyMuPDF (`fitz`) for one-off PDF link extraction (see `data/`)

## Run

```bash
uv run uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000.

The SQLite database (`workout_tracker.db`) is created automatically on first run.

## Pages

- **Workouts** (`/`) — create a workout by date, then log sets (exercise, reps, weight)
  against it. Exercise names autocomplete from previously logged exercises.
- **Program** (`/program`) — read-only view of Jeff Nippard's Ultimate PPL Program,
  Phase 1 (Weeks 1–6). Exercise names link out to their YouTube demo video where one
  was found. Parsed from `data/` at request time via `app/program.py`.

## Project layout

```
app/
  main.py       # FastAPI routes
  models.py     # SQLModel: Workout, Exercise, ExerciseSet
  db.py         # SQLite engine/session
  program.py    # parses data/ into weeks/days/exercises for the Program tab
  templates/    # Jinja2 pages
  static/       # CSS
data/
  ppl_phase1.csv               # source of truth for program structure/content
  ppl_phase1.pdf                # original export, kept only for its embedded YouTube links
  exercise_video_links.json     # exercise name -> YouTube URL, extracted from the PDF
```

`exercise_video_links.json` was generated once by cross-referencing PDF link
annotations against the exercise names in the CSV (see git history for the
extraction script). If the program source data changes, that mapping needs
to be regenerated manually — there's no automated pipeline for it.
