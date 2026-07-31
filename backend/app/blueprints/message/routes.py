from flask import Blueprint, jsonify

message_bp = Blueprint("message", __name__, url_prefix="/messages")


@message_bp.route("", methods=["GET"])
def list_messages():
    return jsonify({"messages": []})
