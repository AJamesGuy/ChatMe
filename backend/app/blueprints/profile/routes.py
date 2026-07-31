from flask import Blueprint, jsonify

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("", methods=["GET"])
def get_profile():
    return jsonify({"profile": {"display_name": "", "bio": ""}})
