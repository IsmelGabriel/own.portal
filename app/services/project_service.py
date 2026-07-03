from app.models.project import Project
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from app.utils.errors import ResourceExistsError

def create_project(
    title,
    description=None,
    repo_url=None,
    image_url=None,
    live_url=None,
    technologies=None
):
    if Project.query.filter_by(title=title).first():
        raise ResourceExistsError(f"Project with name '{title}' already exists.")

    project = Project(
        title=title,
        description=description,
        repo_url=repo_url,
        image_url=image_url,
        live_url=live_url,
        technologies=technologies
    )

    db.session.add(project)
    db.session.commit()
    return project

def get_all_projects():
    return Project.query.order_by(Project.created_at.desc()).all()
