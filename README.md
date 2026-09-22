# The Whole Bible in Daily Sermonettes — Web App

A modular Flask web application that presents the *Whole Bible in Daily
Sermonettes* guide (Old Testament, 183 days; New Testament, 91 days) as a
browsable, self-contained daily devotional — with reading progress,
search, and a JSON API, and no database setup or login required to use it.

## Features

- **Daily sermonette reading** for all 274 days (183 OT + 91 NT), browsable by book or by day, with previous/next paging and left/right arrow-key navigation.
- **"Read the original" prompt.** Clicking or pressing Enter/Space on the "A Voice from Church History" block opens a confirmation dialog offering to open that expositor's actual sermons/commentary/articles in a new tab — but only when a real, stable, freely-accessible archive is known to exist (see `app/data/expositor_sources.py`). Expositors without a known free full-text source (e.g., authors still under active commercial copyright with no publisher-sanctioned free archive) render as plain, non-interactive text — the app never guesses at or fabricates a link.
- **Dark / light mode toggle**, top-right of every page. The choice is remembered (`localStorage`) and applied before first paint, so there's no flash of the wrong theme on load; it also respects the OS-level `prefers-color-scheme` the first time a visitor arrives with no saved preference.
- **Reading progress**, saved per-browser via an anonymous cookie (no account needed) — mark a day read, see per-testament completion, and jump to your next unread day from the home page.
- **Search** across every day's title, chapters, themes, expositor insight, and application question.
- **JSON API** exposing the same data (`/api/day/<testament>/<n>`, `/api/books/<testament>`, `/api/search`).

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Then open **http://localhost:5000**. A SQLite database file is created
automatically at `instance/progress.db` the first time you run it (used
only for anonymous, cookie-based "mark as read" progress — no personal
data, no login).

Run the test suite with:

```bash
pytest
```

## Project layout

```
bible_app/
├── run.py                     # dev entry point (python run.py)
├── requirements.txt
├── app/
│   ├── __init__.py            # application factory (create_app)
│   ├── config.py              # Dev / Prod / Testing config classes
│   ├── extensions.py          # shared SQLAlchemy instance
│   ├── models.py              # pure dataclasses: BookIntro, DayEntry, Guide
│   ├── db_models.py           # SQLAlchemy model: ReadingProgress
│   ├── reader_identity.py     # anonymous cookie-based reader token
│   ├── progress_service.py    # business logic for marking/reading progress
│   ├── search_service.py      # in-memory search across the guide
│   ├── utils.py                # slugify() and small helpers
│   ├── data/
│   │   ├── loader.py           # normalizes raw content into a Guide object
│   │   ├── expositor_sources.py # stable free-source links for "read the original" (only where one genuinely exists)
│   │   ├── content_data.py     # NT book intros + expositor bios (source content)
│   │   ├── content_data_ot.py  # OT book intros + expositor bios (source content)
│   │   ├── days_part*.py       # NT daily sermonette content (91 days)
│   │   ├── ot_days_part*.py    # OT daily sermonette content (183 days)
│   │   └── sermon_extra.py     # opening line / scene / prayer builders
│   ├── blueprints/
│   │   ├── main/                # home page
│   │   ├── devotional/          # /read/<testament>/... — the core reading UX
│   │   ├── progress/             # /progress — dashboard + mark-as-read endpoint
│   │   ├── search/               # /search — keyword search UI
│   │   └── api/                  # /api/... — JSON endpoints
│   ├── templates/               # Jinja2 templates
│   └── static/{css,js}/         # styling and small progressive-enhancement JS
└── tests/
    ├── conftest.py
    ├── test_data_loader.py      # content integrity checks (counts, fields, links)
    └── test_routes.py           # HTTP-level smoke tests for every route
```

## Why this structure

- **Content is data, not code-with-side-effects.** Everything under
  `app/data/*.py` is plain Python lists/dicts of strings — no Flask, no
  I/O. `app/data/loader.py` is the single seam that turns that raw
  content into normalized, typed objects (`app/models.py`). This means
  the content can be tested, reused, or exported (e.g., to JSON, to a
  different framework) without touching a single Flask import.
- **Blueprints separate concerns, not just URLs.** `devotional` only
  knows how to render reading pages; `progress` only knows how to
  persist and report completion; `search` only knows how to query.
  Each blueprint imports the services it needs (`progress_service`,
  `search_service`) rather than reaching into another blueprint.
- **No login, but still personal.** Reading progress is tied to a random
  token stored in a long-lived cookie (`app/reader_identity.py`), so
  progress persists across visits on the same browser without requiring
  an account, email, or password.
- **The JSON API is a first-class citizen.** `/api/day/<testament>/<n>`
  and `/api/books/<testament>` expose the exact same normalized data the
  HTML templates use, so a future mobile app, CLI, or static-site export
  could be built on top without duplicating content logic.

## Extending it

- **Add a new day or book:** edit the relevant `app/data/*.py` file (the
  structure mirrors the existing entries) — no other code changes
  needed; the loader and routes pick it up automatically.
- **Swap storage:** `progress_service.py` is the only place that talks to
  the database, so swapping SQLite for Postgres is a one-line change to
  `SQLALCHEMY_DATABASE_URI` in `config.py` (via the `DATABASE_URL`
  environment variable) — no application code changes required.
- **Add real user accounts:** `reader_identity.py` is intentionally the
  only place that establishes "who is asking" — introducing login later
  means changing that module's `get_reader_token()` implementation, not
  every route.
- **Deploy:** the app is a standard Flask app; run it behind `gunicorn`
  (already in `requirements.txt`) in production, e.g.
  `gunicorn 'run:app' -w 4 -b 0.0.0.0:8000`, and set `FLASK_ENV=production`.

## Content notes

Expositor insights throughout the guide are paraphrased summaries of each
teacher's well-documented public teaching on a passage, not verbatim
quotations. Scripture is referenced by chapter and verse rather than
reproduced at length — keep an NLT Bible (app, site, or print) open
alongside this guide for the text itself.
