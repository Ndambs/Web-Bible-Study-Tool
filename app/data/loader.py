# -*- coding: utf-8 -*-
"""
Turns the raw, hand-authored content modules (book intros, day entries,
expositor bios, and the sermonette-building helpers) into one normalized,
immutable Guide object that the rest of the app queries through simple
dictionaries — no Flask, no I/O, fully unit-testable on its own.

Loading is done once per process and cached in _GUIDE. Call get_guide()
from anywhere in the app to retrieve it.
"""
from typing import Dict, List

from ..models import BookIntro, DayEntry, ChapterNote, Expositor, Guide
from ..utils import slugify, ref_to_slug

from . import content_data as nt_content
from . import content_data_ot as ot_content
from . import days_part1, days_part2, days_part3, days_part4
from . import ot_days_part1, ot_days_part2, ot_days_part3, ot_days_part4
from . import ot_days_part5, ot_days_part6, ot_days_part7, ot_days_part8
from . import sermon_extra as sx
from .expositor_sources import SOURCE_MAP

_GUIDE: Guide = None


def _raw_nt_days() -> List[dict]:
    return (days_part1.DAYS_1 + days_part2.DAYS_2 +
            days_part3.DAYS_3 + days_part4.DAYS_4)


def _raw_ot_days() -> List[dict]:
    return (ot_days_part1.OT_DAYS_1 + ot_days_part2.OT_DAYS_2 +
            ot_days_part3.OT_DAYS_3 + ot_days_part4.OT_DAYS_4 +
            ot_days_part5.OT_DAYS_5 + ot_days_part6.OT_DAYS_6 +
            ot_days_part7.OT_DAYS_7 + ot_days_part8.OT_DAYS_8)


def _build_book_intros(raw_intros, testament: str) -> List[BookIntro]:
    out = []
    for order, entry in enumerate(raw_intros):
        name, subtitle, author, audience, hist, purpose = entry
        out.append(BookIntro(
            testament=testament,
            slug=slugify(name),
            name=name,
            subtitle=subtitle,
            author=author,
            audience=audience,
            historical_setting=hist,
            purpose=purpose,
            order=order,
        ))
    return out


def _intro_lookup_raw() -> Dict[str, tuple]:
    """Name -> raw 6-tuple, exactly as sermon_extra.setting_scene_for expects."""
    lookup = {}
    for entry in ot_content.BOOK_INTROS_OT:
        lookup[entry[0]] = entry
    for entry in nt_content.BOOK_INTROS:
        lookup[entry[0]] = entry
    return lookup


def _book_slug_for(day_book: str, book_to_intro_names: Dict[str, list]) -> str:
    names = book_to_intro_names.get(day_book) or [day_book]
    return slugify(names[0])


def _build_days(raw_days: List[dict], testament: str,
                 book_to_intro_names: Dict[str, list],
                 intro_lookup_raw: Dict[str, tuple]) -> List[DayEntry]:
    out = []
    for idx, d in enumerate(raw_days):
        chapters = tuple(ChapterNote(label=lab, note=note) for lab, note in d["chapters"])
        themes = tuple(d["themes"])
        opening = sx.opening_line_for(d["book"], d["ref"], d["title"], themes[0])
        scene = sx.setting_scene_for(d["book"], intro_lookup_raw, book_to_intro_names)
        prayer = sx.build_prayer(idx, themes[0])
        exp_key, exp_text = d["expositor"]
        out.append(DayEntry(
            testament=testament,
            day_number=d["day"],
            slug=ref_to_slug(d["book"], d["ref"]),
            book=d["book"],
            book_slug=_book_slug_for(d["book"], book_to_intro_names),
            ref=d["ref"],
            title=d["title"],
            chapters=chapters,
            themes=themes,
            expositor_key=exp_key,
            expositor_insight=exp_text,
            reflect=d["reflect"],
            opening_line=opening,
            setting_scene=scene,
            prayer=prayer,
            index_in_testament=idx,
        ))
    return out


def _build_expositors() -> Dict[str, Expositor]:
    merged = dict(nt_content.EXPOSITORS)
    merged.update(ot_content.EXPOSITORS_OT_ADD)
    out = {}
    for key, bio in merged.items():
        if "," in bio:
            name, rest = bio.split(",", 1)
            name = name.strip()
        else:
            name, rest = bio, ""
        source_url, source_label = SOURCE_MAP.get(key, (None, None))
        out[key] = Expositor(key=key, name=name, bio=bio,
                              source_url=source_url, source_label=source_label)
    return out


def load_guide() -> Guide:
    intro_lookup_raw = _intro_lookup_raw()

    ot_book_names = [e[0] for e in ot_content.BOOK_INTROS_OT]
    ot_map = sx.make_ot_map(ot_book_names)
    nt_map = sx.NT_BOOK_TO_INTRO

    ot_intros = _build_book_intros(ot_content.BOOK_INTROS_OT, "OT")
    nt_intros = _build_book_intros(nt_content.BOOK_INTROS, "NT")

    ot_days = _build_days(_raw_ot_days(), "OT", ot_map, intro_lookup_raw)
    nt_days = _build_days(_raw_nt_days(), "NT", nt_map, intro_lookup_raw)

    expositors = _build_expositors()

    all_intros = tuple(ot_intros + nt_intros)
    all_days = tuple(ot_days + nt_days)

    books_by_slug = {b.slug: b for b in all_intros}
    days_by_key = {(d.testament, d.day_number): d for d in all_days}
    days_by_slug = {f"{d.testament.lower()}-{d.slug}": d for d in all_days}

    days_by_book_slug: Dict[str, list] = {}
    for testament, days, book_map in (("OT", ot_days, ot_map), ("NT", nt_days, nt_map)):
        for d in days:
            names = book_map.get(d.book) or [d.book]
            for n in names:
                days_by_book_slug.setdefault(slugify(n), []).append(d)

    return Guide(
        book_intros=all_intros,
        days=all_days,
        expositors=expositors,
        books_by_slug=books_by_slug,
        days_by_key=days_by_key,
        days_by_slug=days_by_slug,
        days_by_book_slug=days_by_book_slug,
    )


def get_guide() -> Guide:
    global _GUIDE
    if _GUIDE is None:
        _GUIDE = load_guide()
    return _GUIDE
