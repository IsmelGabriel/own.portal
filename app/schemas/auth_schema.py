from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    document_number = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))
