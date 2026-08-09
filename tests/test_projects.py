import pytest
from app.models.project import Project
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

        user = User.query.filter_by(document_number="999999999").first()
        if not user:
            hashed_pw = bcrypt.hashpw("adminpass".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = User(
                name="Admin Pruebas",
                document_number="999999999",
                email="admin@test.com",
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


def test_project_model_creation(app, db):
    """Verifica que un objeto Project se instancie y persista en PostgreSQL con sus campos."""
    with app.app_context():
        # Crear un proyecto
        project = Project(
            title="Proyecto de Prueba",
            description="Descripción detallada del proyecto",
            technologies="Python, Flask, Pytest",
            repo_url="https://github.com/prueba"
        )
        db.session.add(project)
        db.session.commit()

        # Recuperar de la base de datos
        retrieved_project = Project.query.filter_by(title="Proyecto de Prueba").first()

        assert retrieved_project is not None
        assert retrieved_project.title == "Proyecto de Prueba"
        assert retrieved_project.technologies == "Python, Flask, Pytest"
        assert retrieved_project.created_at is not None

        # Limpieza
        db.session.delete(retrieved_project)
        db.session.commit()


def test_add_project_authenticated(client, admin_token):
    """Envía POST /api/projects con JWT válido y payload y verifica el 201 Created."""
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }
    payload = {
        "title": "Nuevo API Project",
        "description": "Creado desde pytest",
        "technologies": "Vue, Node",
        "repo_url": "https://github.com/api"
    }

    response = client.post('/api/projects/', json=payload, headers=headers)

    assert response.status_code == 201
    data = response.get_json()
    assert "Project created successfully" in data.get("msg", "")
    assert "project_id" in data
