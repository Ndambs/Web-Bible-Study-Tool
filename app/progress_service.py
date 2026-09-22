# -*- coding: utf-8 -*-
from typing import Dict, Set

from .extensions import db
from .db_models import ReadingProgress
from .data.loader import get_guide


def mark_day(reader_token: str, testament: str, day_number: int, done: bool) -> None:
    testament = testament.upper()
    existing = ReadingProgress.query.filter_by(
        reader_token=reader_token, testament=testament, day_number=day_number
    ).first()
    if done and not existing:
        db.session.add(ReadingProgress(reader_token=reader_token, testament=testament,
                                        day_number=day_number))
        db.session.commit()
    elif not done and existing:
        db.session.delete(existing)
        db.session.commit()


def get_completed_set(reader_token: str, testament: str) -> Set[int]:
    testament = testament.upper()
    rows = ReadingProgress.query.filter_by(reader_token=reader_token, testament=testament).all()
    return {r.day_number for r in rows}


def is_day_done(reader_token: str, testament: str, day_number: int) -> bool:
    testament = testament.upper()
    return ReadingProgress.query.filter_by(
        reader_token=reader_token, testament=testament, day_number=day_number
    ).first() is not None


def get_stats(reader_token: str) -> Dict[str, dict]:
    guide = get_guide()
    totals = {"OT": 0, "NT": 0}
    for d in guide.days:
        totals[d.testament] += 1

    out = {}
    for testament in ("OT", "NT"):
        done = get_completed_set(reader_token, testament)
        total = totals[testament]
        out[testament] = {
            "completed": len(done),
            "total": total,
            "percent": round(100 * len(done) / total) if total else 0,
            "completed_days": sorted(done),
        }
    return out


def next_unread_day(reader_token: str, testament: str):
    """Return the day_number of the first not-yet-completed day in a
    testament, or None if every day is done (or none exist)."""
    guide = get_guide()
    done = get_completed_set(reader_token, testament)
    days = [d for d in guide.days if d.testament == testament]
    for d in days:
        if d.day_number not in done:
            return d.day_number
    return None
