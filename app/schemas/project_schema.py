from marshmallow import Schema, fields, validate

class ProjectSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=False, allow_none=True)
    repo_url = fields.Str(required=False, allow_none=True)
    image_url = fields.Str(required=False, allow_none=True)
    live_url = fields.Str(required=False, allow_none=True)
    technologies = fields.Str(required=False, allow_none=True)
