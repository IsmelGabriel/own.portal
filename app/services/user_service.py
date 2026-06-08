import bcrypt
from app.extensions import db
from app.models.user import User
from app.models.role import Role

def create_user(name, document_number, email, phone, role_name, password):
    """
    Create a new user.
    Password will be hashed using bcrypt.
    """
    # Check if user already exists
    if User.query.filter_by(document_number=document_number).first():
        raise ValueError("User with this document number already exists.")

    if User.query.filter_by(email=email).first():
        raise ValueError("User with this email already exists.")

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        raise ValueError(f"Role '{role_name}' does not exist.")

    # Hash the password
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)

    new_user = User(
        name=name,
        document_number=document_number,
        email=email,
        phone=phone,
        role_id=role.id,
        password_hash=hashed_pw.decode('utf-8')
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user
