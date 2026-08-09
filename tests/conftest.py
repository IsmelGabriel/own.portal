import pytest
import os
from app import create_app
from app.extensions import db as _db

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "Z10T1K1K3YS3CR3TT35T_EXTENDED_32B_KEY"
    WTF_CSRF_ENABLED = False

@pytest.fixture(scope="session")
def app():
    """
    Instancia y configura la aplicación Flask para pruebas.
    """
    _app = create_app(config_class=TestConfig)
    yield _app

@pytest.fixture(scope="session")
def db(app):
    """
    Configura y prepara la base de datos de pruebas.
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def client(app):
    """
    Proporciona un cliente de pruebas de Flask.
    """
    return app.test_client()
