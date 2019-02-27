import os

from flask import render_template, flash, redirect, url_for, current_app, \
    send_from_directory, request, abort, Blueprint
from flask_login import login_required, current_user

from merapy.models import User, Role, ProjectSpider


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    projects = ProjectSpider.query.filter_by(author_id=current_user.id)
    if current_user.is_admin:
        projects = ProjectSpider.query
    projects_num = projects.count()
    running = 0
    data = 0
    for project in projects:
        if project.status_spider == 'Running':
            running += 1
        if project.data == 2:
            data += 1
    user = User.query.count()
    return render_template('main/index.html', projects_num=projects_num, running=running,
                           data=data, user=user)
