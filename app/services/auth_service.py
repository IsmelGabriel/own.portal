import bcrypt
from flask_jwt_extended import create_access_token
from app.models.user import User

def authenticate_user(document_number, password):
    """
    Authenticate user by document_number and password.
    Returns JWT token if successful, None otherwise.
    """
    user = User.query.filter_by(document_number=document_number).first()

    if user and bcrypt.checkpw(
        password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    ):
        # Create token with identity (user.id) and claims (role)
        additional_claims = {"role": user.role.name}
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        return {"access_token": access_token, "role": user.role.name}
    return None
