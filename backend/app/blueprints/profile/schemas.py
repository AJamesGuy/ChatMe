from marshmallow import Schema, fields


class ProfileSchema(Schema):
    display_name = fields.String(required=True)
    bio = fields.String(load_default="")
