# -*- coding: utf-8 -*-
import json


def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Daily Sermonettes" in resp.data or b"Whole Bible" in resp.data


def test_book_list_ot(client):
    resp = client.get("/read/ot/books")
    assert resp.status_code == 200
    assert b"Genesis" in resp.data


def test_book_list_nt(client):
    resp = client.get("/read/nt/books")
    assert resp.status_code == 200
    assert b"Matthew" in resp.data


def test_invalid_testament_404s(client):
    resp = client.get("/read/xx/books")
    assert resp.status_code == 404


def test_day_view_first_and_last(client):
    resp = client.get("/read/ot/day/1")
    assert resp.status_code == 200
    resp = client.get("/read/ot/day/183")
    assert resp.status_code == 200
    resp = client.get("/read/ot/day/184")
    assert resp.status_code == 404

    resp = client.get("/read/nt/day/1")
    assert resp.status_code == 200
    resp = client.get("/read/nt/day/91")
    assert resp.status_code == 200
    resp = client.get("/read/nt/day/92")
    assert resp.status_code == 404


def test_book_detail(client):
    resp = client.get("/read/ot/books/genesis")
    assert resp.status_code == 200
    assert b"Beginnings" in resp.data


def test_mark_and_unmark_progress(client):
    resp = client.post("/progress/mark", data=json.dumps({
        "testament": "ot", "day_number": 1, "done": True
    }), content_type="application/json")
    assert resp.status_code == 200
    payload = resp.get_json()
    assert payload["ok"] is True
    assert payload["stats"]["completed"] == 1

    day_page = client.get("/read/ot/day/1")
    assert b"Marked as read" in day_page.data

    resp = client.post("/progress/mark", data=json.dumps({
        "testament": "ot", "day_number": 1, "done": False
    }), content_type="application/json")
    assert resp.get_json()["stats"]["completed"] == 0


def test_progress_dashboard(client):
    resp = client.get("/progress/")
    assert resp.status_code == 200


def test_search(client):
    resp = client.get("/search/?q=faith")
    assert resp.status_code == 200
    resp = client.get("/search/?q=")
    assert resp.status_code == 200


def test_api_day(client):
    resp = client.get("/api/day/ot/1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["day_number"] == 1
    assert data["testament"] == "OT"
    assert "chapters" in data


def test_api_books(client):
    resp = client.get("/api/books/NT")
    assert resp.status_code == 200
    data = resp.get_json()
    assert any(b["name"] == "Matthew" for b in data)


def test_api_search(client):
    resp = client.get("/api/search?q=grace")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_day_with_known_source_is_clickable(client):
    resp = client.get("/read/ot/day/7")  # ferguson has a known source
    html = resp.data.decode()
    assert 'id="voice-block"' in html
    assert "data-source-url=" in html


def test_day_without_known_source_is_not_clickable(client):
    resp = client.get("/read/ot/day/1")  # kidner has no known source
    html = resp.data.decode()
    assert 'id="voice-block"' not in html
    assert "data-source-url=" not in html


def test_theme_toggle_and_modal_present_on_every_page(client):
    for path in ("/", "/read/ot/day/1", "/progress/", "/search/?q=faith"):
        html = client.get(path).data.decode()
        assert 'id="theme-toggle"' in html
        assert 'id="source-modal"' in html

