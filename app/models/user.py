from app.extensions import db

class User(db.Model):
    """User model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    document_number = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    last_session = db.Column(db.DateTime, nullable=True)
    current_session = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=db.func.now())
    created_at = db.Column(db.DateTime, nullable=True, default=db.func.now())

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False, default=1)

    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    status = db.relationship('Status', backref=db.backref('user_status', lazy=True))

    def __repr__(self):
        return f"<User {self.name}>"
