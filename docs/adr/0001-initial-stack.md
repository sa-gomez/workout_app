# 1. Initial stack: FastAPI + SQLModel/SQLite, managed with uv

Date: 2026-07-10

## Status

Accepted

## Context

Starting a basic fitness tracker web app from scratch. Needed a Python web
framework, a storage approach, and a project/dependency manager.

## Decision

- **uv** for project and dependency management (`uv init --app`, `uv add`,
  `uv run`).
- **FastAPI** over Flask, for async support and auto-generated docs, even
  though the app is currently server-rendered HTML rather than a JSON API.
- **Server-rendered Jinja2 templates** rather than a separate frontend
  (React/etc.) — the app is simple CRUD (create workout, log sets) and
  doesn't need a client-side framework.
- **SQLModel over SQLite** rather than a plain JSON file — gives real
  querying (e.g. distinct exercises for autocomplete, sets-per-workout
  joins) without needing a database server.

## Consequences

- SQLite file (`workout_tracker.db`) is local disk state — not suitable for
  multi-instance deployment without moving to a real Postgres-style DB or
  adding a persistent volume (relevant if deployed somewhere like Render
  with ephemeral disks).
- No test suite was set up initially; changes are verified by running the
  dev server and driving routes manually (see AGENTS.md).
- Newer Starlette (bundled via FastAPI) requires `TemplateResponse(request,
  name, context)` with `request` as a positional arg, not inside the
  context dict — this differs from a lot of older FastAPI tutorials/examples
  and caused a `TypeError: unhashable type: 'dict'` during initial setup.
