import unittest

from app import create_app
from app.extensions import db
from app.models import ChatRoom, User


class BlueprintTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def _create_user(self, username, chat_room):
        user = User(username=username, display_name=username.title(), chat_room_id=chat_room.id, role="user")
        user.set_password("secret")
        db.session.add(user)
        db.session.commit()
        return user

    def test_create_chatroom_route_assigns_admin_role(self):
        chat_room = ChatRoom(access_code="TEST-ROOM-1", name="Seed Room")
        db.session.add(chat_room)
        db.session.commit()

        creator = self._create_user("creator", chat_room)

        response = self.client.post(
            "/user/chatrooms",
            json={"name": "Alpha Room", "user_id": creator.id},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["chat_room"]["name"], "Alpha Room")
        access_code = response.get_json()["chat_room"]["access_code"]
        self.assertRegex(access_code, r"^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$")

        updated_creator = User.query.get(creator.id)
        self.assertEqual(updated_creator.role, "admin")

    def test_only_creator_can_change_chatroom_name_and_generate_access_code(self):
        chat_room = ChatRoom(access_code="TEST-ROOM-2", name="Seed Room")
        db.session.add(chat_room)
        db.session.commit()

        creator = self._create_user("creator", chat_room)
        other_user = self._create_user("member", chat_room)

        response = self.client.post(
            "/user/chatrooms",
            json={"name": "Alpha Room", "user_id": creator.id},
        )
        created_room = ChatRoom.query.filter_by(access_code=response.get_json()["chat_room"]["access_code"]).first()

        self.client.put(
            f"/user/chatrooms/{created_room.id}/name",
            json={"name": "Changed by member", "user_id": other_user.id},
        )
        self.assertEqual(ChatRoom.query.get(created_room.id).name, "Alpha Room")

        response = self.client.post(
            f"/user/chatrooms/{created_room.id}/access-code",
            json={"user_id": other_user.id},
        )
        self.assertEqual(response.status_code, 403)

        response = self.client.put(
            f"/user/chatrooms/{created_room.id}/name",
            json={"name": "Changed by creator", "user_id": creator.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChatRoom.query.get(created_room.id).name, "Changed by creator")

        response = self.client.post(
            f"/user/chatrooms/{created_room.id}/access-code",
            json={"user_id": creator.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get_json()["chat_room"]["access_code"], "TEST-ROOM-2")

    def test_join_chatroom_assigns_user_role(self):
        chat_room = ChatRoom(access_code="TEST-ROOM-3", name="Seed Room")
        db.session.add(chat_room)
        db.session.commit()

        user = self._create_user("joiner", chat_room)

        response = self.client.post(
            f"/user/chatrooms/{chat_room.id}/join",
            json={"user_id": user.id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["user"]["role"], "user")
        self.assertEqual(User.query.get(user.id).role, "user")

    def test_get_user_chatrooms_returns_404_for_unknown_user(self):
        response = self.client.get("/chatrooms/user/1")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "user not found")


if __name__ == "__main__":
    unittest.main()
