from flask import render_template, flash, redirect, url_for, current_app, \
    send_from_directory, request, abort, Blueprint
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from merapy.decorators import admin_required
from merapy.models import User, ProjectSpider, Role, Server
from merapy.extensions import db
from merapy.blueprints import data_view

project_bp = Blueprint('project', __name__)


@project_bp.route('/')
@login_required
def index():
    user_projects = {}
    if current_user.is_admin:
        for user in User.query:
            user_projects.setdefault(user.username, set())
        for project in ProjectSpider.query:
            user = User.query.filter_by(id=project.author_id).first()
            user_projects[user.username].add(project)
    else:
        user_projects.setdefault(current_user.username, set())
        for project in ProjectSpider.query.filter_by(author_id=current_user.id).all():
            user_projects[current_user.username].add(project)

    return render_template('project/spiders.html', user_projects=user_projects)


@project_bp.route('/start/<project_id>')
@login_required
def start(project_id):
    project = ProjectSpider.query.filter_by(id=project_id).first()
    if project.schedule_spider:
        project.have_data()
        flash('Schedule Successful!', 'success')
    else:
        flash('Schedule Failed', 'danger')
    return redirect(url_for('.index'))


@project_bp.route('/stop/<project_id>')
@login_required
def stop(project_id):
    project = ProjectSpider.query.filter_by(id=project_id).first()
    if project.cancel_spider:
        flash('Stop Successful!', 'success')
    else:
        flash('Stop Failed', 'danger')
    return redirect(url_for('.index'))


@project_bp.route('/delete/<project_id>')
@login_required
def delete(project_id):
    project = ProjectSpider.query.filter_by(id=project_id).first()
    server = Server.query.filter_by(id=project.server_id).first()
    if project.delete_project:  # 删除在爬虫服务器上的项目
        try:
            data_view.delete(project.id)  # 从删除该项目的爬取数据
        except:
            pass
        db.session.delete(project)  # 删除数据库的记录
        db.session.commit()
        flash('Delete Successful!', 'success')
    else:
        flash('Delete Failed', 'danger')
    server.delete_project()  # 跟新数据库服务器的记录
    return redirect(url_for('.index'))


