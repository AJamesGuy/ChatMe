from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.extensions import db, cache, limiter
from app.models import ChatRoom, User
from app.utils.auth import encode_token, token_required

from .schemas import LoginUserSchema, RegisterUserSchema, UpdateSettingsSchema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")  # Limit to 5 requests per minute
def register_user():
    schema = RegisterUserSchema()
    try:
        payload = schema.load(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return jsonify({"errors": exc.messages}), 400

    existing_user = User.query.filter_by(username=payload["username"]).first()
    if existing_user:
        return jsonify({"error": "username already exists"}), 409

    user = User(
        username=payload["username"],
        display_name=payload["display_name"],
        role="user",
        chat_room_id=None,
    )
    user.set_password(payload["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "user created", "user": {"id": user.id, "username": user.username}}), 201


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")  # Limit to 10 requests per minute
def login_user():
    schema = LoginUserSchema()
    try:
        payload = schema.load(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return jsonify({"errors": exc.messages}), 400

    user = User.query.filter_by(username=payload["username"]).first()
    if not user or not user.check_password(payload["password"]):
        return jsonify({"error": "invalid credentials"}), 401

    user.is_online = True
    token = encode_token(user.id)
    db.session.commit()
    return jsonify({"message": "logged in", "user": {"id": user.id, "username": user.username}, "token": token}), 200


@auth_bp.route("/settings", methods=["PUT"])
@limiter.limit("5 per minute")  # Limit to 5 requests per minute
@token_required
def update_settings(user_id):
    schema = UpdateSettingsSchema()
    try:
        payload = schema.load(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return jsonify({"errors": exc.messages}), 400

    user = User.query.get_or_404(user_id)
    if "username" in payload:
        user.username = payload["username"]
    if "password" in payload:
        user.set_password(payload["password"])
    if "email" in payload:
        user.email = payload["email"]

    db.session.commit()
    return jsonify({"message": "settings updated"}), 200
