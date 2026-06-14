import bcrypt
from datetime import datetime
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import User

def authenticate_user(document_number, password):
    """
    Authenticate user by document_number and password.
    Returns JWT token if successful, None otherwise.
    """
    user = User.query.filter_by(document_number=document_number).first()

    if user and not user.status.status:
        return {"error": "User is not active"}

    if user and bcrypt.checkpw(
        password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    ):
        user.last_session = user.current_session
        user.current_session = datetime.now()
        db.session.commit()

        additional_claims = {"role": user.role.name}
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        return {"access_token": access_token, "role": user.role.name}
    return None
