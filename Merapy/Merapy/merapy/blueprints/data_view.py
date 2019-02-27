from os.path import dirname, realpath

from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import login_required, current_user


from merapy.models import User, Role,ProjectSpider, Server
from merapy.forms.settings import *
from merapy.extensions import db
import pymongo

data_view_bp = Blueprint('data_view', __name__)


# def down(project_id):
#     project = ProjectSpider.query.filter_by(id=project_id).first()
#     server = Server.query.filter_by(id=project.server_id).first()
#     ip, user, pwd = server.server_ip, server.username, server.password
#     try:
#         db_url = project.spiderSettings.db_url
#     except:
#         db_url = None
#     if db_url == 'default' or not db_url:
#         db_url = 'mongodb://%s:%s@%s:27017/admin' % (user, pwd, ip)
#     client = pymongo.MongoClient(db_url)
#
#     try:
#         db_name = project.spiderSettings.db_name
#     except:
#         db_name = current_user.username
#     db = client[db_name]
#
#     try:
#         collection = project.spiderSettings.collection
#     except:
#         collection = db.list_collection_names()[0]
#
#     data = db[collection].find(projection={'_id': False})
#     key = db[collection].find(projection={'_id': False}).limit(1).next()
#     client.close()
#     path = dirname(realpath(__file__))[:-32] + '/../download/download/' + '%s.txt' % project.project_name
#     with open(path, 'w', encoding='UTF-8') as f:
#         for i in key:
#             f.write(i + '\t')
#         f.write('\n')
#         for item in data:
#             for key in item:
#                 f.write(item[key] + '\t')
#             f.write('\n')
#         f.close()


@data_view_bp.route('/')
@login_required
def index():
    project_data = {}
    if current_user.is_admin:
        for user in User.query:
            project_data.setdefault(user.username, set())

        for project in ProjectSpider.query.filter_by(data=2):
            user = User.query.filter_by(id=project.author_id).first()
            project_data[user.username].add(project)
        for project in ProjectSpider.query.filter_by(data=1):
            if project.status_spider == 'Finished':
                user = User.query.filter_by(id=project.author_id).first()
                try:
                    project.have_down()
                    project_data[user.username].add(project)
                except:
                    flash('%s haven\'t crawl any data or download server error' % project.project_name, 'danger')

    else:
        project_data.setdefault(current_user.username, set())
        for project in ProjectSpider.query.filter_by(data=2).all():
            if project.author_id == current_user.id:
                project_data[current_user.username].add(project)
        for project in ProjectSpider.query.filter_by(data=1).all():
            if project.author_id == current_user.id:
                if project.status_spider == 'Finished':
                    try:
                        project.have_down()
                        project_data[current_user.username].add(project)
                    except:
                        flash('%s haven\'t crawl any data' % project.project_name, 'danger')

    return render_template('data_view/list.html', project_data=project_data)


@data_view_bp.route('/info/<project_id>')
@login_required
def info(project_id):
    try:
        project = ProjectSpider.query.filter_by(id=project_id).first()
        server = Server.query.filter_by(id=project.server_id).first()
        ip, user, pwd = server.server_ip, server.username, server.password
        try:
            db_url = project.spiderSettings.db_url
        except:
            db_url = None
        if db_url == 'default' or not db_url:
            db_url = 'mongodb://%s:%s@%s:27017/admin' % (user, pwd, ip)
        client = pymongo.MongoClient(db_url)

        try:
            db_name = project.spiderSettings.db_name
        except:
            db_name = current_user.username
        db = client[db_name]

        try:
            collection = project.spiderSettings.collection
        except:
            collection = db.list_collection_names()[0]

        data = db[collection].find(projection={'_id': False}).limit(120)
        key = db[collection].find(projection={'_id': False}).limit(1).next()
        client.close()
        return render_template('data_view/view.html', data=data, name=project.project_name, key=key)
    except:
        return redirect(url_for('.index'))


@data_view_bp.route('/delete/<project_id>')
@login_required
def delete(project_id):
    project = ProjectSpider.query.filter_by(id=project_id).first()
    server = Server.query.filter_by(id=project.server_id).first()
    ip, user, pwd = server.server_ip, server.username, server.password
    db_url = project.spiderSettings.db_url
    if db_url == 'default':
        db_url = 'mongodb://%s:%s@%s:27017/admin' % (user, pwd, ip)
    try:
        db = pymongo.MongoClient(db_url)[project.spiderAuthor.username]
        db.drop_collection(project.project_name)
        project.delete_data()
    except:
        flash('Delete data failed!', 'danger')
    return redirect(url_for('.index'))

