from marshmallow import Schema, fields


class MessageSchema(Schema):
    body = fields.String(required=True)
