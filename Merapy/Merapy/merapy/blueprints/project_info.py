from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from merapy.decorators import admin_required
from merapy.models import User, Role,ProjectSpider, SpiderSettings, SpiderRules, SpiderItem
from merapy.forms.settings import *

project_info_bp = Blueprint('project_info', __name__)


@project_info_bp.route('query/<projects_id>')
@login_required
def query(projects_id):
    form = SpiderSettingsForm()
    project = ProjectSpider.query.filter_by(id=projects_id).first()
    settings = SpiderSettings.query.filter_by(projectSpider_id=projects_id).first()
    rules = SpiderRules.query.filter_by(projectSpider_id=projects_id)
    items = SpiderItem.query.filter_by(projectSpider_id=projects_id)
    return render_template('project_info/info.html', form=form, project=project, settings=settings, rules=rules, items=items)
