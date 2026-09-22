# -*- coding: utf-8 -*-
from dataclasses import asdict

from flask import Blueprint, jsonify, abort, request

from ...data.loader import get_guide
from ...search_service import search as search_days

bp = Blueprint("api", __name__, url_prefix="/api")


def _day_to_dict(day):
    data = asdict(day)
    data["chapters"] = [asdict(c) for c in day.chapters]
    return data


def _book_to_dict(book):
    return asdict(book)


@bp.route("/books/<testament>")
def books(testament):
    testament = testament.upper()
    if testament not in ("OT", "NT"):
        abort(404)
    guide = get_guide()
    return jsonify([_book_to_dict(b) for b in guide.book_intros if b.testament == testament])


@bp.route("/day/<testament>/<int:day_number>")
def day(testament, day_number):
    testament = testament.upper()
    guide = get_guide()
    d = guide.days_by_key.get((testament, day_number))
    if not d:
        abort(404)
    return jsonify(_day_to_dict(d))


@bp.route("/search")
def search_api():
    query = request.args.get("q", "")
    testament = request.args.get("testament")
    results = search_days(query, testament=testament)
    return jsonify([_day_to_dict(d) for d in results])
