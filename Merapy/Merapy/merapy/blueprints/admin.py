from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from merapy.decorators import admin_required
from merapy.models import User, Role, ProjectSpider, Server
from merapy.forms.service import ServiceForm
from merapy.extensions import db
from merapy.blueprints import data_view

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/service', methods=['GET', 'POST'])
@login_required
@admin_required
def view_service():
    servers = Server.query.all()
    form = ServiceForm()
    if form.validate_on_submit():
        n_server = Server(
            server_name=form.server_name.data,
            server_ip=form.server_ip.data,
            scrapyd_port=form.scrapyd_port.data,
            username=form.username.data,
            password=form.password.data,
            project_num=0,
        )
        db.session.add(n_server)
        db.session.commit()
        return redirect(url_for('.view_service'))
    return render_template('admin/server.html', form=form, servers=servers)


@admin_bp.route('/service/delete/<server_id>')
@login_required
@admin_required
def delete(server_id):
    projects = ProjectSpider.query.filter_by(server_id=server_id).all()
    for project_ in projects:
        project = ProjectSpider.query.filter_by(id=project_.id).first()
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
    server = Server.query.filter_by(id=server_id).first()
    db.session.delete(server)
    db.session.commit()
    return redirect(url_for('.view_service'))

