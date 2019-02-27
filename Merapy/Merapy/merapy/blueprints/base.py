from flask import render_template, flash, redirect, url_for, current_app, Blueprint
from flask_login import login_required, current_user

from merapy.models import User, Role

base_bp = Blueprint('base', __name__)


@base_bp.route('/')
def index():
    if current_user.is_authenticated:
        role = Role.query.filter_by(id=current_user.role_id).first()
        return render_template('base/base.html', role=role)
    else:
        return redirect(url_for('auth.login'))
