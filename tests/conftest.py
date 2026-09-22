# -*- coding: utf-8 -*-
import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    app = create_app("testing")
    yield app
    with app.app_context():
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
