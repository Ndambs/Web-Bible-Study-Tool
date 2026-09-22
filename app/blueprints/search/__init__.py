# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

from ...search_service import search

bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("/")
def results():
    query = request.args.get("q", "").strip()
    testament = request.args.get("testament") or None
    matches = search(query, testament=testament) if query else []
    return render_template("search_results.html", query=query, matches=matches,
                            testament=testament)
