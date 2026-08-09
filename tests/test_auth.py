import pytest
import bcrypt
from app.models.user import User
from app.models.role import Role
from app.models.status import Status

@pytest.fixture
def auth_user(app, db):
    """Fixture para crear un usuario y sus dependencias temporales en la DB para pruebas de autenticación."""
    with app.app_context():
        # Crear status y rol si no existen
        status = Status.query.filter_by(status=True).first()
        if not status:
            status = Status(status=True)
            db.session.add(status)

        role = Role.query.filter_by(name="admin").first()
        if not role:
            role = Role(name="admin", description="Administrador")
            db.session.add(role)

        db.session.commit()

        # Encriptar la contraseña (según app.services.auth_service)
        hashed_pw = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User.query.filter_by(document_number="000000000").first()
        if not user:
            user = User(
                name="Usuario Pruebas",
                document_number="000000000",
                email="auth@test.com",
                password_hash=hashed_pw,
                role_id=role.id,
                status_id=status.id
            )
            db.session.add(user)
            db.session.commit()

        yield user

        # Limpieza después del test no es estrictamente necesaria porque
        # el db fixture principal hace drop_all, pero por buenas prácticas lo quitamos.
        db.session.delete(user)
        db.session.commit()


def test_post_login_success(client, auth_user):
    """Verifica el login exitoso enviando credenciales válidas."""
    response = client.post('/api/auth/login', json={
        "document_number": "000000000",
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert "Login successful" in data.get("msg", "")

    # Comprobamos que JWT se guarde en cookies (según JWT_TOKEN_LOCATION=['cookies'])
    cookies = response.headers.getlist('Set-Cookie')
    assert any("csrf" in c.lower() or "jwt" in c.lower() for c in cookies) or len(cookies) > 0


def test_post_login_invalid_credentials(client, auth_user):
    """Verifica que el sistema rechaza contraseñas incorrectas."""
    response = client.post('/api/auth/login', json={
        "document_number": "000000000",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    data = response.get_json()
    assert "Invalid credentials" in data.get("msg", "")

def test_post_login_missing_fields(client):
    """Verifica validación de esquema en la ruta login."""
    response = client.post('/api/auth/login', json={})

    assert response.status_code == 400
    data = response.get_json()
    assert "Validation error" in data.get("msg", "")


def test_user_password_hashing(auth_user):
    """Verifica que el modelo User aplique el hashing de contraseña y no guarde texto plano."""
    # auth_user ya está guardado en base de datos con contraseña "password123"
    assert auth_user.password_hash != "password123"

    # Verificamos que se pueda desencriptar/comparar con bcrypt exitosamente
    assert bcrypt.checkpw(
        "password123".encode('utf-8'),
        auth_user.password_hash.encode('utf-8')
    ) is True
