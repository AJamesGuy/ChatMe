from marshmallow import Schema, fields, validate

class RegisterUserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
    display_name = fields.String(required=True, validate=validate.Length(min=1, max=80))


class LoginUserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class UpdateSettingsSchema(Schema):
    email = fields.Email(load_default=None)
    username = fields.String(validate=validate.Length(min=3, max=80))
    password = fields.String(load_only=True, validate=validate.Length(min=6))
