from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.project_service import create_project, update_project, delete_project
from app.utils.decorators import require_role
from app.schemas.project_schema import ProjectSchema
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

project_bp = Blueprint('project', __name__)

@project_bp.route('/', methods=['POST'])
@jwt_required()
@require_role('admin')
def add_project():
    """
    Endpoint to create a new project.
    Only accessible by users with 'admin' role.
    """
    data = request.get_json()

    schema = ProjectSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        logger.warning(f"Project validation error: {err.messages}")
        return jsonify({"msg": "Validation error", "errors": err.messages}), 400

    try:
        new_project = create_project(
            title=validated_data['title'],
            description=validated_data.get('description'),
            repo_url=validated_data.get('repo_url'),
            image_url=validated_data.get('image_url'),
            live_url=validated_data.get('live_url'),
            technologies=validated_data.get('technologies')
        )
        return jsonify({
            "msg": "Project created successfully",
            "project_id": new_project.id
        }), 201
    except Exception as e:
        logger.error(f"Error during project creation: {str(e)}", exc_info=True)
        return jsonify({"msg": str(e)}), 400

@project_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
@require_role('admin')
def edit_project(project_id):
    data = request.get_json()
    try:
        updated = update_project(project_id, **data)
        return jsonify({"msg": "Project updated successfully"}), 200
    except Exception as e:
        logger.error(f"Error updating project: {str(e)}", exc_info=True)
        return jsonify({"msg": str(e)}), 400

@project_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
@require_role('admin')
def remove_project(project_id):
    try:
        delete_project(project_id)
        return jsonify({"msg": "Project deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}", exc_info=True)
        return jsonify({"msg": str(e)}), 400
