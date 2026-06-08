import os
import bcrypt
from flask.cli import FlaskGroup
from app import create_app
from app.extensions import db
from app.models.role import Role
from app.models.user import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("seed_db")
def seed_db():
    """Seeds the database with initial roles and admin user."""
    db.create_all()

    # Create roles if they don't exist
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Administrator')
        db.session.add(admin_role)

    guest_role = Role.query.filter_by(name='invitado').first()
    if not guest_role:
        guest_role = Role(name='invitado', description='Guest user')
        db.session.add(guest_role)

    db.session.commit()

    # Create admin user
    admin_doc = os.getenv('ADMIN_INITIAL_DOC', '123456789')
    admin_pass = os.getenv('ADMIN_INITIAL_PASS', 'admin123')

    admin_user = User.query.filter_by(document_number=admin_doc).first()
    if not admin_user:
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(admin_pass.encode('utf-8'), salt)

        admin_user = User(
            name='Super Admin',
            document_number=admin_doc,
            email='admin@portal.local',
            phone='0000000000',
            role_id=admin_role.id,
            password_hash=hashed_pw.decode('utf-8')
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user created with document: {admin_doc}")
    else:
        print("Admin user already exists.")

if __name__ == '__main__':
    cli()
