from marshmallow import Schema, fields, validate

class SkillSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    icon_class = fields.Str(required=False, allow_none=True, validate=validate.Length(max=100))
    description = fields.Str(required=False, allow_none=True)
