from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import set_access_cookies
from app.services.auth_service import authenticate_user
from app.schemas.auth_schema import LoginSchema
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint.
    Expects JSON or Form Data.
    """
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # Fallback to empty dict if neither is available
    if not data:
        data = {}

    schema = LoginSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({"msg": "Validation error", "errors": err.messages}), 400

    result = authenticate_user(
        document_number=validated_data['document_number'],
        password=validated_data['password']
    )

    if result:
        if "error" in result:
            return jsonify({"msg": result["error"]}), 403

        response = jsonify({"msg": "Login successful", "role": result["role"]})
        set_access_cookies(response, result["access_token"])
        return response, 200

    return jsonify({"msg": "Invalid credentials"}), 401
