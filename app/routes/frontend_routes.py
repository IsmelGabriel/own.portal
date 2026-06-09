from flask import Blueprint, render_template, redirect, url_for, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies
from app.models.user import User
from app.models.role import Role
from app.utils.decorators import require_role

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    return redirect(url_for('frontend.login'))

@frontend_bp.route('/login')
def login():
    return render_template('login.html')

@frontend_bp.route('/dashboard')
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
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
    roles = Role.query.all()
    return render_template('create_user.html', roles=roles)
