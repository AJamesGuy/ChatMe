from marshmallow import Schema, fields, validate


class CreateChatroomSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    user_id = fields.Int(required=True)


class UpdateChatroomNameSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    user_id = fields.Int(required=True)


class GenerateAccessCodeSchema(Schema):
    user_id = fields.Int(required=True)
