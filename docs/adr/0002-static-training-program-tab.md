# 2. Program tab: CSV as source of truth, PDF only for video links

Date: 2026-07-10

## Status

Accepted

## Context

Wanted a read-only reference tab showing Jeff Nippard's Ultimate PPL
Program (Phase 1, Weeks 1-6) with links to exercise demo videos on YouTube.

Two exports of the same Google Sheet were available:
- A **CSV** export: clean, well-structured rows (week, day, exercise, sets,
  reps, RPE, rest, substitutions, notes), but plain text — no hyperlinks,
  since CSV can't carry cell-level hyperlink formatting.
- A **PDF** export: retains the sheet's hyperlinks (exercise names link to
  YouTube demos) as PDF link annotations, but the export's page/column
  layout is fragmented — a wide sheet got split across ~90 pages by column
  group, so the PDF's *text* layout is unreliable for anything beyond
  link extraction.

Direct API access to the source Google Sheet was not available in this
session (the connected Google Drive account couldn't see the file — likely
a different Google account was viewing it than the one connected here).

## Decision

- **CSV is the sole source of program *structure and content*** — parsed by
  `app/program.py` into `ProgramWeek -> ProgramDay -> ProgramExercise`.
- **PDF is used only to recover YouTube links**, via `PyMuPDF` (`fitz`)
  reading link annotations (`page.get_links()`) and the text inside each
  link's bounding box (`page.get_textbox(rect)`), matched against the exact
  exercise names already known from the CSV.
- The resulting `{exercise name: youtube url}` mapping was extracted once
  and committed as a static file: `data/exercise_video_links.json`. There
  is **no automated pipeline** re-deriving this at request time from the
  PDF — `app/program.py` just loads the JSON.

## Extraction notes (for regenerating the JSON if the source changes)

- Matching is by **exact exercise name string**, restricted to the known
  set of names from the CSV — a naive "grab every link on the page" pass
  over-matches, because substitution-column text (e.g. "DB Bulgarian Split
  Squat") can independently contain a full exercise name ("Squat") as a
  trailing word, pointing to a different video than the main exercise.
  Taking the **first page-order occurrence** per name resolves this, since
  the main "Exercise" column appears before the substitution columns.
- A few exercise names wrap across two lines in the PDF, splitting into two
  separate link annotations with the same URI (e.g. "Squeeze-Only Triceps
  Pressdown + Stretch-" / "Only Overhead Triceps Extension"). These need
  concatenation to match the CSV's single-string exercise name; one case
  needed a manual fix because the line wrapped mid-hyphenated-word with no
  space to rejoin on.

## Consequences

- Program content updates require re-exporting the CSV and dropping it in
  at `data/ppl_phase1.csv`.
- Video links go stale silently if the source sheet's hyperlinks change —
  regenerating `exercise_video_links.json` is a manual PDF re-export +
  re-run of the extraction, not something wired into the app.
- `data/ppl_phase1.pdf` (~330KB) is committed to the repo despite being a
  one-time extraction source, so the extraction is reproducible without
  needing Drive access again.
