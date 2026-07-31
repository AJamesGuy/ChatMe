from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class ChatRoom(db.Model):
    __tablename__ = "chat_rooms"

    id = db.Column(db.Integer, primary_key=True)
    access_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, default="ChatMe Room")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    users = db.relationship("User", back_populates="chat_room", cascade="all, delete-orphan")
    messages = db.relationship("Message", back_populates="chat_room", cascade="all, delete-orphan")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    is_online = db.Column(db.Boolean, default=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user", server_default="user")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    chat_room_id = db.Column(db.Integer, db.ForeignKey("chat_rooms.id"), nullable=True)
    chat_room = db.relationship("ChatRoom", back_populates="users")
    messages = db.relationship("Message", back_populates="author", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    chat_room_id = db.Column(db.Integer, db.ForeignKey("chat_rooms.id"), nullable=False)

    author = db.relationship("User", back_populates="messages")
    chat_room = db.relationship("ChatRoom", back_populates="messages")
