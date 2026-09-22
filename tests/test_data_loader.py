# -*- coding: utf-8 -*-
from app.data.loader import get_guide


def test_day_counts():
    guide = get_guide()
    ot_days = [d for d in guide.days if d.testament == "OT"]
    nt_days = [d for d in guide.days if d.testament == "NT"]
    assert len(ot_days) == 183
    assert len(nt_days) == 91


def test_day_numbers_are_sequential_and_unique():
    guide = get_guide()
    for testament, expected_total in (("OT", 183), ("NT", 91)):
        numbers = sorted(d.day_number for d in guide.days if d.testament == testament)
        assert numbers == list(range(1, expected_total + 1))


def test_every_day_resolves_an_expositor():
    guide = get_guide()
    for d in guide.days:
        assert d.expositor_key in guide.expositors, f"missing expositor for {d.testament} day {d.day_number}"


def test_every_day_has_core_fields():
    guide = get_guide()
    for d in guide.days:
        assert d.title
        assert d.ref
        assert d.chapters
        assert d.themes
        assert d.reflect
        assert d.opening_line
        assert d.prayer


def test_lookup_dicts_are_consistent():
    guide = get_guide()
    for d in guide.days:
        assert guide.days_by_key[(d.testament, d.day_number)] is d
        assert guide.days_by_slug[f"{d.testament.lower()}-{d.slug}"] is d


def test_book_slugs_have_at_least_one_day():
    guide = get_guide()
    non_review_books = [b for b in guide.book_intros]
    for b in non_review_books:
        days = guide.days_by_book_slug.get(b.slug)
        assert days, f"no days found for book {b.name} ({b.slug})"


def test_source_map_keys_are_valid_expositors():
    from app.data.expositor_sources import SOURCE_MAP
    guide = get_guide()
    for key in SOURCE_MAP:
        assert key in guide.expositors, f"SOURCE_MAP has unknown expositor key: {key}"


def test_expositors_with_source_have_both_url_and_label():
    guide = get_guide()
    for exp in guide.expositors.values():
        if exp.source_url:
            assert exp.source_label
        if exp.source_label:
            assert exp.source_url
