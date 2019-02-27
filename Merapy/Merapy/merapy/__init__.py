# -*-coding:utf-8-*-
import os

import click
from flask import Flask, render_template
from flask_login import current_user
from scrapyd_api import ScrapydAPI

from merapy.blueprints.base import base_bp
from merapy.blueprints.auth import auth_bp
from merapy.blueprints.main import main_bp
from merapy.blueprints.project import project_bp
from merapy.blueprints.add_project import add_project_bp
from merapy.blueprints.project_info import project_info_bp
from merapy.blueprints.data_view import data_view_bp
from merapy.blueprints.admin import admin_bp
from merapy.blueprints.manual import manual_pb

from merapy.extensions import bootstrap, db, login_manager, moment, csrf

from merapy.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('merapy')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(base_bp)
    app.register_blueprint(main_bp, url_prefix='/main')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(project_bp, url_prefix='/project')
    app.register_blueprint(add_project_bp, url_prefix='/add')
    app.register_blueprint(project_info_bp, url_prefix='/pjf')
    app.register_blueprint(data_view_bp, url_prefix='/data')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(manual_pb, url_prefix='/manual')


def register_commands(app):
    @app.cli.command()
    @click.option('--user', default=3, help='Quantity of users, default is 3.')
    def forge(user):
        from merapy.fakes import fake_admin, fake_user, fake_project, init_server
        from merapy.models import Role, User

        db.drop_all()
        db.create_all()

        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Generating %d users...' % user)
        fake_user(user)
        click.echo('fake project')
        fake_project()
        click.echo('init server')
        init_server()


