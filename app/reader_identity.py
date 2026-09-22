# -*- coding: utf-8 -*-
import uuid

from flask import current_app, g, request


def get_reader_token() -> str:
    """Return the current visitor's anonymous reader token, creating one
    in flask.g if this request doesn't have the cookie yet. The token is
    written to the response cookie by `attach_reader_cookie` (registered
    as an after_request hook in the app factory)."""
    if "reader_token" in g:
        return g.reader_token

    cookie_name = current_app.config["USER_COOKIE_NAME"]
    token = request.cookies.get(cookie_name)
    if not token:
        token = str(uuid.uuid4())
        g.reader_token_is_new = True
    g.reader_token = token
    return token


def attach_reader_cookie(response):
    if g.get("reader_token_is_new"):
        cookie_name = current_app.config["USER_COOKIE_NAME"]
        max_age = current_app.config["USER_COOKIE_MAX_AGE"]
        response.set_cookie(cookie_name, g.reader_token, max_age=max_age,
                             httponly=True, samesite="Lax")
    return response
