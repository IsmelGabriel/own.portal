from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.skill_service import create_skill
from app.utils.decorators import require_role
from app.schemas.skill_schema import SkillSchema
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

skill_bp = Blueprint('skill', __name__)

@skill_bp.route('/', methods=['POST'])
@jwt_required()
@require_role('admin')
def add_skill():
    """
    Endpoint to create a new skill.
    Only accessible by users with 'admin' role.
    """
    data = request.get_json()

    schema = SkillSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        logger.warning(f"Skill validation error: {err.messages}")
        return jsonify({"msg": "Validation error", "errors": err.messages}), 400

    try:
        new_skill = create_skill(
            name=validated_data['name'],
            icon_class=validated_data.get('icon_class'),
            description=validated_data.get('description')
        )
        return jsonify({
            "msg": "Skill created successfully",
            "skill_id": new_skill.id
        }), 201
    except Exception as e:
        logger.error(f"Error during skill creation: {str(e)}", exc_info=True)
        return jsonify({"msg": str(e)}), 400
