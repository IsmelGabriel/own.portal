from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.user_service import create_user
from app.utils.decorators import require_role
from app.schemas.user_schema import UserRegistrationSchema
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['POST'])
@jwt_required()
@require_role('admin')
def register_user():
    """
    Endpoint to create a new user.
    Only accessible by users with 'admin' role.
    """
    data = request.get_json()

    schema = UserRegistrationSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        logger.warning(f"User registration validation error: {err.messages}")
        return jsonify({"msg": "Validation error", "errors": err.messages}), 400

    try:
        new_user = create_user(
            name=validated_data['name'],
            document_number=validated_data['document_number'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            role_name=validated_data['role_name'],
            password=validated_data['password']
        )
        return jsonify({
            "msg": "User created successfully",
            "user_id": new_user.id
        }), 201
    except ValueError as e:
        logger.warning(f"User registration failed: {str(e)}")
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        logger.error(f"Internal server error during user registration: {str(e)}", exc_info=True)
        return jsonify({"msg": "Internal server error"}), 500
