from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
from app.extensions import db, migrate, jwt
import os

def create_app(config_class=None):
    """Factory to create and configure the Flask app."""
    if config_class is None:
        if os.getenv('FLASK_ENV') == 'production':
            config_class = ProductionConfig
        else:
            config_class = DevelopmentConfig
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.frontend_routes import frontend_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(frontend_bp)

    from flask import redirect, url_for
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return redirect(url_for('frontend.login'))

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return redirect(url_for('frontend.login'))

    return app
