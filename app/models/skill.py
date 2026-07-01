from app.extensions import db

class Skill(db.Model):
    """Skill model for the portfolio."""
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon_class = db.Column(db.String(100), nullable=True) # e.g. fa-brands fa-python
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=db.func.now())

    def __repr__(self):
        return f"<Skill {self.name}>"
