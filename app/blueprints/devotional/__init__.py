# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, g, redirect, url_for

from ...data.loader import get_guide
from ...reader_identity import get_reader_token
from ...progress_service import get_completed_set, is_day_done

bp = Blueprint("devotional", __name__, url_prefix="/read/<testament>")

VALID_TESTAMENTS = {"ot": "OT", "nt": "NT"}


@bp.url_value_preprocessor
def pull_testament(endpoint, values):
    raw = values.pop("testament", None)
    if raw not in VALID_TESTAMENTS:
        abort(404)
    g.testament = VALID_TESTAMENTS[raw]
    g.testament_slug = raw


@bp.url_defaults
def add_testament(endpoint, values):
    if "testament" not in values and getattr(g, "testament_slug", None):
        values["testament"] = g.testament_slug


@bp.route("/books")
def book_list():
    guide = get_guide()
    books = [b for b in guide.book_intros if b.testament == g.testament]
    token = get_reader_token()
    completed = get_completed_set(token, g.testament)

    books_with_progress = []
    for b in books:
        days = guide.days_by_book_slug.get(b.slug, [])
        done = sum(1 for d in days if d.day_number in completed)
        books_with_progress.append({
            "book": b,
            "day_count": len(days),
            "first_day": days[0].day_number if days else None,
            "done": done,
        })

    return render_template("book_list.html", books=books_with_progress,
                            testament=g.testament, testament_slug=g.testament_slug)


@bp.route("/books/<book_slug>")
def book_detail(book_slug):
    guide = get_guide()
    book = guide.books_by_slug.get(book_slug)
    if not book or book.testament != g.testament:
        abort(404)
    days = guide.days_by_book_slug.get(book_slug, [])
    token = get_reader_token()
    completed = get_completed_set(token, g.testament)

    return render_template("book_detail.html", book=book, days=days,
                            completed=completed, testament=g.testament,
                            testament_slug=g.testament_slug)


@bp.route("/day/<int:day_number>")
def day_view(day_number):
    guide = get_guide()
    day = guide.days_by_key.get((g.testament, day_number))
    if not day:
        abort(404)

    total = sum(1 for d in guide.days if d.testament == g.testament)
    prev_day = day_number - 1 if day_number > 1 else None
    next_day = day_number + 1 if day_number < total else None

    token = get_reader_token()
    done = is_day_done(token, g.testament, day_number)
    expositor = guide.expositors.get(day.expositor_key)

    return render_template(
        "day.html", day=day, expositor=expositor, done=done,
        prev_day=prev_day, next_day=next_day, total=total,
        testament=g.testament, testament_slug=g.testament_slug,
    )


@bp.route("/")
def testament_home():
    return redirect(url_for("devotional.book_list", testament=g.testament_slug))
