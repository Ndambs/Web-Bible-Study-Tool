# -*- coding: utf-8 -*-
import re

_slug_strip_re = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Turn 'Titus & Philemon' into 'titus-philemon', '1 Corinthians' into
    '1-corinthians', etc. Deterministic and dependency-free."""
    text = text.lower().strip()
    text = text.replace("'", "")
    text = _slug_strip_re.sub("-", text)
    return text.strip("-")


def ref_to_slug(book_label: str, ref: str) -> str:
    """Build a stable per-day slug like 'genesis-1-5' from the book label
    and the human-readable reference string."""
    base = f"{book_label} {ref}" if book_label not in ref else ref
    return slugify(base)
