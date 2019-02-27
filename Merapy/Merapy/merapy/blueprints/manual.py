from flask import render_template, flash, redirect, url_for, current_app, \
    send_from_directory, request, abort, Blueprint
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from merapy.decorators import admin_required
from merapy.models import User, ProjectSpider, Role, Server
from merapy.extensions import db
from merapy.blueprints import data_view

manual_pb = Blueprint('manual_pb', __name__)


@manual_pb.route('/use')
@login_required
def how_use():
    return render_template('manual/how_use.html')





