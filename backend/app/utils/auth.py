from datetime import datetime, timezone, timedelta
from functools import wraps
from jose import jwt
from flask import request, jsonify, current_app
import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

def encode_token(user_id, expires_in=3600):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "token is missing"}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token has expired"}), 401
        except jwt.JWTError:
            return jsonify({"error": "invalid token"}), 401

        return f(user_id, *args, **kwargs)

    return decorated