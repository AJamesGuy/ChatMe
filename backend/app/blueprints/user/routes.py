import random
import string

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.extensions import db, cache, limiter
from app.models import ChatRoom, User
from app.utils import token_required

from .schemas import CreateChatroomSchema, GenerateAccessCodeSchema, UpdateChatroomNameSchema

user_bp = Blueprint("user", __name__, url_prefix="/user")

@token_required
def generate_access_code():
    while True:
        parts = ["".join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)]
        code = "-".join(parts)
        if not ChatRoom.query.filter_by(access_code=code).first():
            return code


@user_bp.route("/create-chatroom", methods=["POST"])
def create_chatroom():
    schema = CreateChatroomSchema()
    try:
        payload = schema.load(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return jsonify({"errors": exc.messages}), 400

    user = User.query.get(payload["user_id"])
    if not user:
        return jsonify({"error": "user not found"}), 404

    chat_room = ChatRoom(
        access_code=generate_access_code(),
        name=payload["name"],
    )
    db.session.add(chat_room)
    db.session.flush()

    user.chat_room_id = chat_room.id
    user.role = "admin"
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "chat room created", "chat_room": {"id": chat_room.id, "access_code": chat_room.access_code, "name": chat_room.name, "role": user.role}}), 201


@user_bp.route("/chatrooms/<int:chatroom_id>/name", methods=["PUT"])
def update_chatroom_name(chatroom_id):
    schema = UpdateChatroomNameSchema()
    try:
        payload = schema.load(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return jsonify({"errors": exc.messages}), 400

    chat_room = ChatRoom.query.get(chatroom_id)
    if not chat_room:
        return jsonify({"error": "chat room not found"}), 404

    user = User.query.get(payload["user_id"])
    if not user or user.chat_room_id != chat_room.id or user.role != "admin":
        return jsonify({"error": "forbidden"}), 403

    chat_room.name = payload["name"]
    db.session.commit()
    return jsonify({"message": "chat room name updated", "chat_room": {"id": chat_room.id, "name": chat_room.name, "access_code": chat_room.access_code}}), 200


@user_bp.route("/chatrooms/<int:chatroom_id>/access-code", methods=["POST"])
def generate_chatroom_access_code(chatroom_id):
    schema = GenerateAccessCodeSchema()
    try:
        payload = schema.load(request.get_json(silent=True) or {})
    except ValidationError as exc:
        return jsonify({"errors": exc.messages}), 400

    chat_room = ChatRoom.query.get(chatroom_id)
    if not chat_room:
        return jsonify({"error": "chat room not found"}), 404

    user = User.query.get(payload["user_id"])
    if not user or user.chat_room_id != chat_room.id or user.role != "admin":
        return jsonify({"error": "forbidden"}), 403

    chat_room.access_code = generate_access_code()
    db.session.commit()
    return jsonify({"message": "access code generated", "chat_room": {"id": chat_room.id, "name": chat_room.name, "access_code": chat_room.access_code}}), 200


@user_bp.route("/chatrooms/<int:chatroom_id>/join", methods=["POST"])
def join_chatroom(chatroom_id):
    user_id = request.get_json(silent=True, default={}).get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    chat_room = ChatRoom.query.get(chatroom_id)
    if not chat_room:
        return jsonify({"error": "chat room not found"}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404

    user.chat_room_id = chat_room.id
    user.role = "user"
    db.session.commit()

    return jsonify({"message": "joined chat room", "chat_room": {"id": chat_room.id, "name": chat_room.name, "access_code": chat_room.access_code}, "user": {"id": user.id, "role": user.role}}), 200
