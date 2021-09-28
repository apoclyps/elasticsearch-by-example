from app import config

if config.DATADOG_TRACE_ENABLED:
    from ddtrace import patch_all

    patch_all()

from flask import Flask
from flask_cors import CORS

from app import views
from app.commands.elasticsearch.indexes import create_indexes, delete_indexes
from lib import logging

ALLOWED_ORIGINS = {
    "development": ["http://localhost:*"],
    "test": ["*"],
}


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config")

    CORS(app, origins=ALLOWED_ORIGINS.get(config.FLASK_ENV, None))

    # Service views
    app.register_blueprint(views.docs)
    app.register_blueprint(views.errors)
    app.register_blueprint(views.healthz)
    app.register_blueprint(views.healthz_public)

    # Register Click commands
    app.cli.add_command(create_indexes)
    app.cli.add_command(delete_indexes)

    # Initialise logging
    logging.init_app(app)

    return app
