import bcrypt
from datetime import datetime, timedelta
import logging
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import User

logger = logging.getLogger(__name__)

def authenticate_user(document_number, password):
    """
    Authenticate user by document_number and password.
    Returns JWT token if successful, None otherwise.
    """
    user = User.query.filter_by(document_number=document_number).first()

    if user and not user.status.status:
        logger.warning(f"Login attempt for inactive user document: {document_number}")
        return {"error": "User is not active"}

    if user and bcrypt.checkpw(
        password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    ):
        user.last_session = user.current_session
        user.current_session = datetime.utcnow()
        db.session.commit()

        additional_claims = {"role": user.role.name}
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=8)
        )
        logger.info(f"Successful login for user ID: {user.id} ({document_number})")
        return {"access_token": access_token, "role": user.role.name}

    logger.warning(f"Failed login attempt for document: {document_number}")
    return None
