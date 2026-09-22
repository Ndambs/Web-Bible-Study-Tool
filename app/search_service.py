# -*- coding: utf-8 -*-
"""
The whole guide is ~275 short entries, so a linear, case-insensitive
substring search is fast enough (sub-millisecond) and needs no external
search engine or index to keep in sync. If the guide grows substantially,
this is the seam where a real search index would slot in without
changing the blueprint that calls it.
"""
from typing import List, Optional

from .data.loader import get_guide
from .models import DayEntry


def _haystack(day: DayEntry) -> str:
    parts = [day.title, day.ref, day.book, day.reflect, day.expositor_insight]
    parts.extend(day.themes)
    parts.extend(c.note for c in day.chapters)
    parts.extend(c.label for c in day.chapters)
    return " \n ".join(parts).lower()


def search(query: str, testament: Optional[str] = None, limit: int = 40) -> List[DayEntry]:
    query = (query or "").strip().lower()
    if not query:
        return []
    guide = get_guide()
    results = []
    for day in guide.days:
        if testament and day.testament != testament.upper():
            continue
        if query in _haystack(day):
            results.append(day)
            if len(results) >= limit:
                break
    return results
