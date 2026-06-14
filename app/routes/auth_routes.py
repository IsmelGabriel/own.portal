from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import set_access_cookies
from app.services.auth_service import authenticate_user

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

    if not data or not data.get('document_number') or not data.get('password'):
        return jsonify({"msg": "Missing document_number or password"}), 400

    result = authenticate_user(
        document_number=data.get('document_number'),
        password=data.get('password')
    )

    if result:
        if "error" in result:
            return jsonify({"msg": result["error"]}), 403

        response = jsonify({"msg": "Login successful", "role": result["role"]})
        set_access_cookies(response, result["access_token"])
        return response, 200

    return jsonify({"msg": "Invalid credentials"}), 401
