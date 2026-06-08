from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def require_role(role_name):
    """
    Decorator to ensure the user has a specific role.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != role_name:
                return jsonify({
                    "msg": f"Access forbidden: requires {role_name} role"
                }), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
