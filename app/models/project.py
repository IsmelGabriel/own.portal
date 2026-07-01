from app.extensions import db

class Project(db.Model):
    """Project model for the portfolio."""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    repo_url = db.Column(db.String(255), nullable=True)
    live_url = db.Column(db.String(255), nullable=True)
    technologies = db.Column(db.String(255), nullable=True) # Comma separated
    created_at = db.Column(db.DateTime, nullable=True, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=db.func.now())

    def __repr__(self):
        return f"<Project {self.title}>"
