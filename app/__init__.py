from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
from app.extensions import db, migrate, jwt
from app.utils.logger_setup import logger
from werkzeug.exceptions import HTTPException
import os
import uuid
from flask import g, request, jsonify

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
    from app.routes.skill_routes import skill_bp
    from app.routes.project_routes import project_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(skill_bp, url_prefix='/api/skills')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    app.register_blueprint(frontend_bp)

    from flask import redirect, url_for
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return redirect(url_for('frontend.login'))

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return redirect(url_for('frontend.login'))

    def mask_sensitive_data(data):
        if not isinstance(data, dict):
            return data
        masked = data.copy()
        for secret_field in ["password", "contrasena", "token", "clave"]:
            if secret_field in masked:
                masked[secret_field] = "********"
        return masked

    # requests logs
    @app.before_request
    def log_request_info():
        g.req_id = str(uuid.uuid4())[:8]

        logger.info(
            f"[Request: {g.req_id}] IN: {request.method} "
            f"{request.url} - IP: {request.remote_addr}"
        )

        if request.is_json:
            data = request.get_json(silent=True)
            logger.info(
                f"[Request: {g.req_id}] Data JSON: "
                f"{mask_sensitive_data(data)}"
                )
        elif request.form:
            logger.info(
                f"[Request: {g.req_id}] Data Form: "
                f"{mask_sensitive_data(request.form.to_dict())}"
                )

        if request.args:
            logger.info(
                f"[Request: {g.req_id}] Args: "
                f"{mask_sensitive_data(request.args.to_dict())}"
                )

    # responses logs
    @app.after_request
    def log_response_info(response):
        req_id = getattr(g, 'req_id', 'N/A')

        if response.is_json:
            response_data = response.get_json(silent=True)

            # Prevent logging huge payloads
            if isinstance(response_data, list) and len(response_data) > 20:
                logger.info(
                    f"[Request: {req_id}] Response: "
                    f"[{len(response_data)} items omitted]"
                )
            elif isinstance(response_data, dict) and len(str(response_data)) > 2000:
                logger.info(
                    f"[Request: {req_id}] Response: "
                    f"[Large payload omitted]"
                )
            else:
                logger.info(
                    f"[Request: {req_id}] Response: "
                    f"{mask_sensitive_data(response_data)}"
                )

        return response
    # errores
    from app.utils.errors import (
    ResourceNotFoundError,
    ResourceExistsError,
    ValidationError
)

    @app.errorhandler(ResourceNotFoundError)
    def handle_resource_not_found(e):
        logger.warning(
            f"ResourceNotFoundError: {str(e)}"
            )
        return jsonify(
            {"error": str(e), "log_id": getattr(g, 'req_id', 'N/A')}
            ), 404

    @app.errorhandler(ResourceExistsError)
    def handle_resource_exists(e):
        logger.warning(
            f"ResourceExistsError: {str(e)}"
            )
        return jsonify(
            {"error": str(e), "log_id": getattr(g, 'req_id', 'N/A')}
            ), 409

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        logger.warning(
            f"ValidationError: {str(e)}"
            )
        return jsonify(
            {"error": str(e), "log_id": getattr(g, 'req_id', 'N/A')}
            ), 400

    @app.errorhandler(PermissionError)
    def handle_permission_error(e):
        logger.warning(
            f"PermissionError: {str(e)}"
            )
        return jsonify(
            {"error": str(e), "log_id": getattr(g, 'req_id', 'N/A')}
            ), 403

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        logger.warning(
            f"HTTPException: {str(e)}"
            )
        return jsonify(
            {"error": str(e), "log_id": getattr(g, 'req_id', 'N/A')}
            ), e.code

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(
            f"Unhandled Exception: {str(e)}",
            exc_info=True
            )
        return jsonify(
            {
                "error": "Internal server error",
                "log_id": getattr(g, 'req_id', 'N/A')
            }
        ), 500

    return app
