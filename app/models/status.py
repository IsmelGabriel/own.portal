from app.extensions import db

class Status(db.Model):
    """Status model."""
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Boolean, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=db.func.now())
    created_at = db.Column(db.DateTime, nullable=True, default=db.func.now())

    def __repr__(self):
        return f"<Status {self.status}>"
