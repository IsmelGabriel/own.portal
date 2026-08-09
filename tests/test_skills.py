import pytest
from app.models.skill import Skill
from flask_jwt_extended import create_access_token
from app.models.role import Role
from app.models.user import User
from app.models.status import Status
import bcrypt

@pytest.fixture
def admin_token(app, db):
    """Fixture para crear un admin y generar su token JWT."""
    with app.app_context():
        status = Status.query.filter_by(status=True).first()
        if not status:
            status = Status(status=True)
            db.session.add(status)

        role = Role.query.filter_by(name="admin").first()
        if not role:
            role = Role(name="admin", description="Administrador")
            db.session.add(role)

        db.session.commit()

        user = User.query.filter_by(document_number="888888888").first()
        if not user:
            hashed_pw = bcrypt.hashpw("adminpass".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = User(
                name="Admin Pruebas 2",
                document_number="888888888",
                email="admin2@test.com",
                password_hash=hashed_pw,
                role_id=role.id,
                status_id=status.id
            )
            db.session.add(user)
            db.session.commit()

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": "admin"}
        )
        yield access_token


def test_skill_model_creation(app, db):
    """Guarda un objeto Skill (name, icon_class) y comprueba su recuperación mediante SQLAlchemy."""
    with app.app_context():
        skill = Skill(
            name="Docker",
            icon_class="fa-brands fa-docker",
            description="Contenedores"
        )
        db.session.add(skill)
        db.session.commit()

        retrieved_skill = Skill.query.filter_by(name="Docker").first()

        assert retrieved_skill is not None
        assert retrieved_skill.name == "Docker"
        assert retrieved_skill.icon_class == "fa-brands fa-docker"

        db.session.delete(retrieved_skill)
        db.session.commit()


def test_add_skill_authenticated(client, admin_token):
    """Envía POST /api/skills con token JWT válido verificando respuesta 201 Created."""
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }
    payload = {
        "name": "Kubernetes",
        "icon_class": "fa-solid fa-server",
        "description": "Orquestación"
    }

    response = client.post('/api/skills/', json=payload, headers=headers)

    assert response.status_code == 201
    data = response.get_json()
    assert "Skill created successfully" in data.get("msg", "")
    assert "skill_id" in data
