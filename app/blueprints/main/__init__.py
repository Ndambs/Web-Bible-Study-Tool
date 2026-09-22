# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

from ...data.loader import get_guide
from ...reader_identity import get_reader_token
from ...progress_service import get_stats, next_unread_day

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    guide = get_guide()
    token = get_reader_token()
    stats = get_stats(token)

    ot_next = next_unread_day(token, "OT")
    nt_next = next_unread_day(token, "NT")

    ot_books = [b for b in guide.book_intros if b.testament == "OT"]
    nt_books = [b for b in guide.book_intros if b.testament == "NT"]

    return render_template(
        "home.html",
        stats=stats,
        ot_next=ot_next,
        nt_next=nt_next,
        ot_total=len(ot_books),
        nt_total=len(nt_books),
        ot_days_total=stats["OT"]["total"],
        nt_days_total=stats["NT"]["total"],
    )


@bp.route("/about")
def about():
    return render_template("about.html")
