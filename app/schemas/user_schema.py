from marshmallow import Schema, fields, validate

class UserRegistrationSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    document_number = fields.String(required=True, validate=validate.Length(min=5, max=50))
    email = fields.Email(required=True)
    phone = fields.String(required=True, validate=validate.Length(min=7, max=20))
    role_name = fields.String(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
