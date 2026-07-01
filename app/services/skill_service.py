from app.models.skill import Skill
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from app.utils.errors import ResourceExistsError

def create_skill(name, icon_class=None, description=None):
    if Skill.query.filter_by(name=name).first():
        raise ResourceExistsError(f"Skill with name '{name}' already exists.")

    skill = Skill(
        name=name,
        icon_class=icon_class,
        description=description
    )

    db.session.add(skill)
    db.session.commit()
    return skill

def get_all_skills():
    return Skill.query.order_by(Skill.created_at.desc()).all()
