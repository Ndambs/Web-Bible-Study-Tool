# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template

from .config import CONFIG_MAP
from .extensions import db
from .reader_identity import get_reader_token, attach_reader_cookie


def create_app(config_name: str = None) -> Flask:
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(CONFIG_MAP.get(config_name, CONFIG_MAP["development"]))

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    from . import db_models  # noqa: F401  (ensures models are registered before create_all)
    with app.app_context():
        db.create_all()

    register_blueprints(app)
    register_error_handlers(app)
    register_context_processors(app)

    app.after_request(attach_reader_cookie)

    return app


def register_blueprints(app: Flask) -> None:
    from .blueprints.main import bp as main_bp
    from .blueprints.devotional import bp as devotional_bp
    from .blueprints.progress import bp as progress_bp
    from .blueprints.search import bp as search_bp
    from .blueprints.api import bp as api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(devotional_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(api_bp)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500


def register_context_processors(app: Flask) -> None:
    @app.context_processor
    def inject_globals():
        from .data.loader import get_guide
        return {
            "reader_token": get_reader_token(),
            "guide_meta": {
                "ot_total": sum(1 for d in get_guide().days if d.testament == "OT"),
                "nt_total": sum(1 for d in get_guide().days if d.testament == "NT"),
            },
        }
