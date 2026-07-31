from marshmallow import Schema, fields


class ChatRoomSchema(Schema):
    name = fields.String(required=True)
