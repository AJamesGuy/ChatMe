from flask import Blueprint, jsonify

from app.models import ChatRoom, User
from app.utils.auth import token_required

chatroom_bp = Blueprint("chatroom", __name__, url_prefix="/chatrooms")


@chatroom_bp.route("", methods=["GET"])
@token_required
def get_user_chatrooms(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404

    room = user.chat_room
    if not room:
        return jsonify({"chat_rooms": []})

    return jsonify({"chat_rooms": [{"id": room.id, "name": room.name, "access_code": room.access_code}]})
