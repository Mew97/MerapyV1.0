# -*-coding:utf-8-*-
import os
from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from merapy.extensions import db


from scrapyd_api import ScrapydAPI


class Role(db.Model):  # 权限角色
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    users = db.relationship('User', back_populates='role')

    @staticmethod
    def init_role():  # 初始化
        roles_permissions_map = {'Administrator', 'User', 'Locked'}

        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
        db.session.commit()


class User(db.Model, UserMixin):  # 用户资料
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)  # 确保名字不重复且建立索引
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(20))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)

    # 用户状态
    locked = db.Column(db.Boolean, default=False)

    # 权限(外键)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')

    projectSpider = db.relationship('ProjectSpider', back_populates='spiderAuthor')

    def __init__(self, **kwargs):  # 在初始化的时候就给一个权限
        super(User, self).__init__(**kwargs)
        self.set_role()

    def set_password(self, password):  # 设置密码
        self.password_hash = generate_password_hash(password)

    def set_role(self):  # 设置权限
        if self.role is None:
            if self.username == current_app.config['MERAPY_ADMIN_NAME']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()
            db.session.commit()

    def validate_password(self, password):  # 验证密码
        return check_password_hash(self.password_hash, password)

    def lock(self):  # 封禁账号
        self.locked = True
        self.role = Role.query.filter_by(name='Locked').first()
        db.session.commit()

    def unlock(self):  # 解锁账号
        self.locked = False
        self.role = Role.query.filter_by(name='User').first()
        db.session.commit()

    @property
    def is_admin(self):
        return self.role.name == 'Administrator'


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_name = db.Column(db.String(20))
    server_ip = db.Column(db.String(20))
    scrapyd_port = db.Column(db.String(5))
    username = db.Column(db.String(10))
    password = db.Column(db.String(30))
    project_num = db.Column(db.Integer)

    project_spider = db.relationship('ProjectSpider', uselist=False, back_populates='spiderServer')

    @property
    def server_status(self):
        try:
            ScrapydAPI('http://%s:%s/' % (self.server_ip, self.scrapyd_port), auth=(self.username, self.password)).list_projects()
            return 'Normal'
        except:
            return 'Error'

    def add_project(self):
        self.project_num += 1
        db.session.commit()

    def delete_project(self):
        self.project_num -= 1
        db.session.commit()


class ProjectSpider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(20), unique=True, index=True)
    spider_name = db.Column(db.String(20))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    data = db.Column(db.Integer, default=0)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))

    spiderSettings = db.relationship('SpiderSettings', uselist=False, back_populates='project_spider', passive_deletes=True)  # 一对一
    spiderRules = db.relationship('SpiderRules', backref='project_spider', passive_deletes=True)
    spiderItem = db.relationship('SpiderItem', backref='project_spider', passive_deletes=True)

    spiderServer = db.relationship('Server', back_populates='project_spider')

    spiderAuthor = db.relationship('User', back_populates='projectSpider')

    def have_data(self):
        self.data = 1
        db.session.commit()

    def have_down(self):
        self.data = 2
        db.session.commit()

    def delete_data(self):
        self.data = 0
        db.session.commit()

    @property
    def scrapyd(self):
        ip = self.spiderServer.server_ip
        port = self.spiderServer.scrapyd_port
        user = self.spiderServer.username
        pwd = self.spiderServer.password
        return ScrapydAPI('http://%s:%s/' % (ip, port), auth=(user, pwd))

    @property
    def schedule_spider(self):
        try:
            self.scrapyd.schedule(self.project_name, self.spider_name)
            return True
        except:
            return False

    @property
    def cancel_spider(self):
        try:
            job_name = self.scrapyd.list_jobs(self.project_name)['node_name']
            self.scrapyd.cancel(self.project_name, job_name)
            return True
        except:
            return False

    @property
    def status_spider(self):
        try:
            status = self.scrapyd.list_jobs(self.project_name)
            if status['running']:
                return 'Running'
            if status['finished']:
                return 'Finished'
            else:
                return 'Normal'
        except:
            return False

    @property
    def delete_project(self):
        try:
            self.scrapyd.delete_project(self.project_name)
            return True
        except:
            return False


class SpiderSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    start_url = db.Column(db.String(256))
    allowed_domains = db.Column(db.String(50))
    collection = db.Column(db.String(20))  # 项目存储的集合

    item_pipelines = db.Column(db.String(20))
    db_url = db.Column(db.String(60))
    db_name = db.Column(db.String(20))  # 选择的数据库名（默认为当前用户的名字

    dynamic = db.Column(db.Boolean)  # 动态网页

    projectSpider_id = db.Column(db.Integer, db.ForeignKey('project_spider.id', ondelete='CASCADE'))

    project_spider = db.relationship('ProjectSpider', back_populates='spiderSettings')


class SpiderRules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restrict_xpaths = db.Column(db.String(100))
    allow = db.Column(db.String(100))
    callback = db.Column(db.Boolean)
    follow = db.Column(db.Boolean)

    projectSpider_id = db.Column(db.Integer, db.ForeignKey('project_spider.id', ondelete='CASCADE'))


class SpiderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(50))
    method = db.Column(db.String(10))
    args = db.Column(db.String(100))
    re = db.Column(db.String(100))

    projectSpider_id = db.Column(db.Integer, db.ForeignKey('project_spider.id', ondelete='CASCADE'))


# 临时表
class SpiderSettings0(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user = db.Column(db.Integer)
    project_name = db.Column(db.String(20))
    spider_name = db.Column(db.String(20))
    start_url = db.Column(db.String(256))
    allowed_domains = db.Column(db.String(50))

    item_pipelines = db.Column(db.String(20))
    db_url = db.Column(db.String(60))
    collection = db.Column(db.String(20))

    dynamic = db.Column(db.Boolean)


class SpiderRules0(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user = db.Column(db.Integer)
    restrict_xpaths = db.Column(db.String(100))
    allow = db.Column(db.String(100))
    callback = db.Column(db.Boolean)
    follow = db.Column(db.Boolean)


class SpiderItem0(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user = db.Column(db.Integer)
    keyword = db.Column(db.String(50))
    method = db.Column(db.String(10))
    args = db.Column(db.String(100))
    re = db.Column(db.String(100))



