# -*- coding: utf-8 -*-
"""
Helper logic to turn the existing day-entry data (chapters, themes,
expositor insight, reflect question) into a fuller "sermonette" — a
self-contained daily devotional that doesn't require outside lookup.
Nothing here invents new biblical claims; it reorganizes and frames
material already authored in the day-entry files, plus short devotional
scaffolding (an opening line, a prayer) built from that same material.
"""

# Maps a day's `book` label to the intro-entry name(s) whose "historical
# setting" sentence should be surfaced as that day's "Setting the Scene."
NT_BOOK_TO_INTRO = {
    "Matthew": ["Matthew"], "Mark": ["Mark"], "Luke": ["Luke"], "John": ["John"],
    "Acts": ["Acts"], "Romans": ["Romans"],
    "1 Corinthians": ["1 Corinthians"], "2 Corinthians": ["2 Corinthians"],
    "Galatians": ["Galatians"], "Ephesians": ["Ephesians"],
    "Philippians": ["Philippians"], "Colossians": ["Colossians"],
    "1 Thessalonians": ["1 & 2 Thessalonians"], "2 Thessalonians": ["1 & 2 Thessalonians"],
    "1 Timothy": ["1 & 2 Timothy and Titus"], "2 Timothy": ["1 & 2 Timothy and Titus"],
    "Titus & Philemon": ["1 & 2 Timothy and Titus", "Philemon"],
    "Hebrews": ["Hebrews"], "James": ["James"],
    "1 Peter": ["1 & 2 Peter"], "2 Peter": ["1 & 2 Peter"],
    "1 John": ["1, 2 & 3 John"], "2 John, 3 John & Jude": ["1, 2 & 3 John", "Jude"],
    "Revelation": ["Revelation"], "Review": [],
}

def make_ot_map(ot_book_names):
    return {name: [name] for name in ot_book_names}

PRAYER_OPENERS = [
    "Father, thank You that {truth}.",
    "Lord God, I praise You that {truth}.",
    "Gracious Father, You have shown me today that {truth}.",
    "Holy God, my heart is stirred to remember that {truth}.",
    "Lord, I come to You grateful that {truth}.",
]
PRAYER_MIDDLES = [
    "Search me now in light of what I've read, and give me an honest, teachable heart.",
    "Help me not merely to admire this truth but to actually live differently because of it today.",
    "Where I have drifted from this truth, draw me gently back to Yourself.",
    "Give me courage to respond obediently to what Your word has just shown me.",
    "Let this truth take root deeply enough to shape my choices, not just my thoughts, today.",
]
PRAYER_CLOSERS = [
    "In Jesus' name, Amen.",
    "I ask this in the name of Jesus Christ, Amen.",
    "Through Christ my Lord, Amen.",
]

PROTECTED_STARTS = ("God", "Jesus", "Christ", "The LORD", "Scripture", "Isaiah",
                     "Israel", "Old Testament", "New Testament", "Chronicles's",
                     "Chronicles'", "Christ's", "God's", "Jesus'", "Genesis's")

def lowercase_first(s):
    s = s.strip()
    if s.endswith("."):
        s = s[:-1]
    if not s:
        return s
    for p in PROTECTED_STARTS:
        if s.startswith(p):
            return s
    return s[0].lower() + s[1:]

def build_prayer(day_index, theme_text):
    truth = lowercase_first(theme_text)
    opener = PRAYER_OPENERS[day_index % len(PRAYER_OPENERS)]
    middle = PRAYER_MIDDLES[(day_index // len(PRAYER_OPENERS)) % len(PRAYER_MIDDLES)]
    closer = PRAYER_CLOSERS[day_index % len(PRAYER_CLOSERS)]
    return opener.format(truth=truth) + " " + middle + " " + closer

def strip_label(sentence, labels=("Historical Setting:", "Audience & Occasion:", "Purpose:")):
    s = sentence.strip()
    for lab in labels:
        if s.startswith(lab):
            return s[len(lab):].strip()
    return s

def setting_scene_for(day_book, intro_lookup, book_to_intro_names):
    names = book_to_intro_names.get(day_book, [])
    if not names:
        return None
    parts = []
    for n in names:
        entry = intro_lookup.get(n)
        if not entry:
            continue
        # entry = (name, subtitle, author, audience, hist, purpose)
        hist = strip_label(entry[4])
        parts.append(hist)
    if not parts:
        return None
    return " ".join(parts)

def opening_line_for(book, ref, title, theme_text):
    truth = lowercase_first(theme_text)
    if book == "Review":
        return f"Pause today to look back before you look ahead: {truth}."
    return f"Come to God's word today in {ref} — \u201c{title}\u201d — and let this truth take root: {truth}."
