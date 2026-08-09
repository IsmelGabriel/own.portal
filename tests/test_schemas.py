from marshmallow import ValidationError
import pytest
from app.schemas.auth_schema import LoginSchema
from app.schemas.project_schema import ProjectSchema
from app.schemas.skill_schema import SkillSchema

def test_login_schema_validation():
    """Valida que LoginSchema exija document_number y password no vacíos."""
    schema = LoginSchema()

    # Payload válido
    valid_payload = {"document_number": "12345678", "password": "mypassword"}
    result = schema.load(valid_payload)
    assert result == valid_payload

    # Payload inválido: campos vacíos
    invalid_payload_empty = {"document_number": "", "password": ""}
    with pytest.raises(ValidationError) as exc:
        schema.load(invalid_payload_empty)
    assert "document_number" in exc.value.messages
    assert "password" in exc.value.messages

    # Payload inválido: sin los campos requeridos
    invalid_payload_missing = {}
    with pytest.raises(ValidationError) as exc:
        schema.load(invalid_payload_missing)
    assert "document_number" in exc.value.messages
    assert "password" in exc.value.messages


def test_project_schema_validation():
    """Valida que ProjectSchema exija title y description de forma correcta."""
    schema = ProjectSchema()

    # Payload válido con campos obligatorios
    valid_payload = {
        "title": "Mi Proyecto",
        "description": "Descripción del proyecto"
    }
    result = schema.load(valid_payload)
    assert result["title"] == "Mi Proyecto"

    # Payload válido con campos opcionales
    valid_payload_full = {
        "title": "Proyecto Completo",
        "description": "Descripción",
        "repo_url": "http://github.com",
        "live_url": "http://misitio.com",
        "technologies": "Python, Flask"
    }
    result_full = schema.load(valid_payload_full)
    assert "repo_url" in result_full

    # Payload inválido: título vacío (longitud mínima es 1)
    invalid_payload_empty_title = {"title": ""}
    with pytest.raises(ValidationError) as exc:
        schema.load(invalid_payload_empty_title)
    assert "title" in exc.value.messages


def test_skill_schema_validation():
    """Valida que SkillSchema exija name y procese icon_class y description opcionales."""
    schema = SkillSchema()

    # Payload válido
    valid_payload = {
        "name": "Python",
        "icon_class": "fa-brands fa-python",
        "description": "Lenguaje de programación"
    }
    result = schema.load(valid_payload)
    assert result["name"] == "Python"
    assert result["icon_class"] == "fa-brands fa-python"

    # Payload inválido: falta el nombre
    invalid_payload = {"description": "Sin nombre"}
    with pytest.raises(ValidationError) as exc:
        schema.load(invalid_payload)
    assert "name" in exc.value.messages
