# -*- coding: utf-8 -*-
"""
Plain dataclasses describing the shape of the guide's content once it has
been loaded and normalized by app.data.loader. Nothing in this module
touches Flask, SQLAlchemy, or the filesystem — it is pure data shape, so
it can be reused by the web app, the API, tests, or a future CLI/export
tool without change.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class ChapterNote:
    label: str
    note: str


@dataclass(frozen=True)
class BookIntro:
    testament: str          # "OT" or "NT"
    slug: str                # url-safe identifier, e.g. "1-corinthians"
    name: str                 # display name, e.g. "1 Corinthians"
    subtitle: str
    author: str               # "Author & Date: ..."
    audience: str             # "Audience & Occasion: ..."
    historical_setting: str   # "Historical Setting: ..."
    purpose: str              # "Purpose: ..."
    order: int                # canonical order within its testament


@dataclass(frozen=True)
class Expositor:
    key: str
    name: str
    bio: str
    source_url: Optional[str] = None
    source_label: Optional[str] = None


@dataclass(frozen=True)
class DayEntry:
    testament: str            # "OT" or "NT"
    day_number: int           # 1-based, independent per testament
    slug: str                 # url-safe slug, e.g. "genesis-1-5"
    book: str                 # raw book label as used in the source data
    book_slug: str            # slug of the mapped BookIntro (may be shared,
                               # e.g. "Titus & Philemon" -> "1-2-timothy-and-titus")
    ref: str                  # human reference, e.g. "Genesis 1-5"
    title: str
    chapters: Tuple[ChapterNote, ...]
    themes: Tuple[str, ...]
    expositor_key: str
    expositor_insight: str
    reflect: str
    opening_line: str
    setting_scene: Optional[str]
    prayer: str
    index_in_testament: int   # 0-based position, for prev/next navigation


@dataclass(frozen=True)
class Guide:
    """The whole loaded, normalized guide."""
    book_intros: Tuple[BookIntro, ...]
    days: Tuple[DayEntry, ...]                 # OT days then NT days, in order
    expositors: dict                            # key -> Expositor
    books_by_slug: dict = field(default_factory=dict)
    days_by_key: dict = field(default_factory=dict)       # (testament, day_number) -> DayEntry
    days_by_slug: dict = field(default_factory=dict)      # slug -> DayEntry
    days_by_book_slug: dict = field(default_factory=dict) # book_slug -> [DayEntry, ...]
