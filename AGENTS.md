# Agent instructions — Workout Tracker

## Stack

- Python, managed with [uv](https://docs.astral.sh/uv/) — use `uv add`/`uv remove` for deps, `uv run` to execute
- FastAPI, server-rendered with Jinja2 templates (no frontend build step, no JS framework)
- SQLModel over SQLite, session-per-request via `Depends(get_session)`

## Commands

```bash
uv run uvicorn app.main:app --reload   # run the dev server
uv sync                                 # install/sync deps after a pull
```

There is no test suite yet. Verify changes by running the server and hitting
routes with `curl`, or exercising the flow in a browser.

## Conventions

- Routes live in `app/main.py`; keep it flat (this app is small — don't split
  into routers/blueprints unless it actually grows past a handful of routes).
- Templates extend `app/templates/base.html`. New top-level pages get a
  `<nav>` link there.
- `TemplateResponse` calls must pass `request` as the first positional arg
  (this Starlette version deprecated the old `{"request": request, ...}`
  dict-based form — see `docs/adr/0002-static-training-program-tab.md` if
  you hit `TypeError: unhashable type: 'dict'` again).
- Date/datetime fields on SQLModel models: import as `import datetime as dt`
  and use `dt.date` / `dt.datetime`, not `from datetime import date` — a
  field named `date` typed as `date` breaks pydantic's model-field
  collection.

## Architecture decisions

See `docs/adr/`. Read the relevant ADR before changing:
- the data model / storage approach
- the Program tab's data pipeline (`app/program.py`, `data/`)

## Where things are

- `app/models.py` — `Workout`, `Exercise`, `ExerciseSet`
- `app/program.py` — parses `data/ppl_phase1.csv` + `data/exercise_video_links.json`
  into the read-only Program tab. `data/ppl_phase1.pdf` is kept only as the
  source the video-link JSON was extracted from — don't treat it as
  structured data, the CSV is the source of truth for program content.
