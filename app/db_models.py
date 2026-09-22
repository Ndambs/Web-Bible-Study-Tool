# -*- coding: utf-8 -*-
"""
Reading-progress persistence. Deliberately login-free: each browser gets
an anonymous, random token stored in a long-lived cookie (see
app.reader_identity), and progress rows are keyed by that token. This
keeps the app usable immediately with zero setup while still persisting
progress across visits on the same device/browser.
"""
from datetime import datetime, timezone

from .extensions import db


class ReadingProgress(db.Model):
    __tablename__ = "reading_progress"

    id = db.Column(db.Integer, primary_key=True)
    reader_token = db.Column(db.String(36), nullable=False, index=True)
    testament = db.Column(db.String(2), nullable=False)   # "OT" or "NT"
    day_number = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint("reader_token", "testament", "day_number",
                             name="uq_reader_day"),
    )

    def __repr__(self):
        return f"<ReadingProgress {self.reader_token[:8]} {self.testament}{self.day_number}>"
