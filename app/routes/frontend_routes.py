from flask import Blueprint, render_template, redirect, url_for, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies
from app.services.user_service import get_user_by_id, get_all_users
from app.services.role_service import get_all_roles
from app.utils.decorators import require_role
from app.models.project import Project
from app.models.skill import Skill

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    skills = Skill.query.order_by(Skill.description.asc()).all()
    return render_template('portfolio.html', projects=projects, skills=skills)

@frontend_bp.route('/login')
def login():
    return render_template('login.html')

@frontend_bp.route('/dashboard')
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    claims = get_jwt()
    return render_template('dashboard.html', user=user, role=claims.get('role'))

@frontend_bp.route('/logout')
def logout():
    response = make_response(redirect(url_for('frontend.login')))
    unset_jwt_cookies(response)
    return response

@frontend_bp.route('/users/new')
@jwt_required()
@require_role('admin')
def create_user_view():
    roles = get_all_roles()
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    claims = get_jwt()
    return render_template('create_user.html', roles=roles, user=user)

@frontend_bp.route('/users/profile/<int:user_id>')
@jwt_required()
def user_profile(user_id):
    user = get_user_by_id(user_id)
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    if str(user_id) != str(current_user_id) and claims.get('role') != 'admin':
        return jsonify({"msg": f"Access forbidden"}), 403
    return render_template('user_profile.html', user=user)

@frontend_bp.route('/users')
@jwt_required()
@require_role('admin')
def list_users_view():
    users = get_all_users()
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    claims = get_jwt()
    return render_template('list_users.html', users=users, user=user)

@frontend_bp.route('/dashboard/skills/new')
@jwt_required()
@require_role('admin')
def create_skill_view():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    return render_template('create_skill.html', user=user)

@frontend_bp.route('/dashboard/projects/new')
@jwt_required()
@require_role('admin')
def create_project_view():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    return render_template('create_project.html', user=user)
