from marshmallow import Schema, fields, validate


class CreateChatroomSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))


class UpdateChatroomNameSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))


class JoinChatroomSchema(Schema):
    access_code = fields.String(required=True, validate=validate.Length(min=19, max=19))
