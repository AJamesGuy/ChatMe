from flask import Blueprint, jsonify

from app.blueprints import auth_bp, chatroom_bp, user_bp

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return jsonify({"message": "ChatMe backend is running"})


@main_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chatroom_bp)
