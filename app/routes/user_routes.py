from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.user_service import create_user
from app.utils.decorators import require_role

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

    required_fields = [
        'name', 'document_number', 'email',
        'phone', 'role_name', 'password'
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"Missing required field: {field}"}), 400

    try:
        new_user = create_user(
            name=data['name'],
            document_number=data['document_number'],
            email=data['email'],
            phone=data['phone'],
            role_name=data['role_name'],
            password=data['password']
        )
        return jsonify({
            "msg": "User created successfully",
            "user_id": new_user.id
        }), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": "Internal server error"}), 500
