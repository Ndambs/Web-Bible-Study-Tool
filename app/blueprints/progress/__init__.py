# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify

from ...reader_identity import get_reader_token
from ...progress_service import mark_day, get_stats
from ...data.loader import get_guide

bp = Blueprint("progress", __name__, url_prefix="/progress")


@bp.route("/")
def dashboard():
    token = get_reader_token()
    stats = get_stats(token)
    guide = get_guide()

    def remaining(testament):
        done = set(stats[testament]["completed_days"])
        days = [d for d in guide.days if d.testament == testament and d.day_number not in done]
        return days[:10]

    return render_template("progress.html", stats=stats,
                            ot_remaining=remaining("OT"), nt_remaining=remaining("NT"))


@bp.route("/mark", methods=["POST"])
def mark():
    token = get_reader_token()
    payload = request.get_json(silent=True) or request.form
    testament = (payload.get("testament") or "").upper()
    day_number = payload.get("day_number")
    done = str(payload.get("done", "true")).lower() in ("1", "true", "yes", "on")

    if testament not in ("OT", "NT") or not day_number:
        return jsonify({"error": "invalid request"}), 400

    mark_day(token, testament, int(day_number), done)
    stats = get_stats(token)[testament]
    return jsonify({"ok": True, "done": done, "stats": stats})
