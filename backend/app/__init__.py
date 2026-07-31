from flask import Flask

from .extensions import db, cache, limiter
from .models import ChatRoom, Message, User  # noqa: F401
from .routes import register_blueprints


def create_app(config_object=None):
    app = Flask(__name__)

    if config_object is None:
        from config import DevelopmentConfig

        app.config.from_object(DevelopmentConfig)
    elif isinstance(config_object, dict):
        app.config.update(config_object)
    else:
        app.config.from_object(config_object)

    db.init_app(app)
    register_blueprints(app)
    cache.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        # db.drop_all()
        db.create_all()

    return app
