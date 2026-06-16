from app.models.role import Role

def get_all_roles():
    """Retrieve all roles."""
    return Role.query.all()
