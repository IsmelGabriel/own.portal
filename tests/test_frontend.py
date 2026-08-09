def test_get_index_page(client):
    """Verifica que la ruta principal responde 200 OK."""
    response = client.get('/')
    assert response.status_code == 200
    # Verificamos renderizado básico
    assert b"<!DOCTYPE html>" in response.data or b"<html" in response.data


def test_get_login_page(client):
    """Verifica que la página de login carga correctamente."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"login" in response.data.lower()


def test_dashboard_protected_route(client):
    """Verifica que el acceso al dashboard sin token JWT es redirigido o bloqueado."""
    response = client.get('/dashboard')
    # Según la configuración en __init__.py, jwt.unauthorized_loader redirige a /login (302)
    # o si se usara el error por defecto sería 401.
    # Validamos que no sea 200 (acceso denegado o redirigido)
    assert response.status_code in [302, 401, 422]

    if response.status_code == 302:
        assert '/login' in response.headers.get('Location', '')
