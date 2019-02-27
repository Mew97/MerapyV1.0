# -*-coding:utf-8-*-
from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from merapy.decorators import admin_required
from merapy.models import User, Role, SpiderSettings0, SpiderRules0, SpiderItem0, \
    ProjectSpider, SpiderSettings, SpiderRules, SpiderItem, Server
from merapy.forms.settings import *
from merapy.extensions import db
from merapy.utils import write_setting, transform

add_project_bp = Blueprint('add_project', __name__)


@add_project_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SpiderSettingsForm()
    form_rules = SpiderRulesForm()
    form_items = SpiderItemForm()
    settings = SpiderSettings0.query.filter_by(user=current_user.id).first()
    rules = SpiderRules0.query.filter_by(user=current_user.id).all()
    items = SpiderItem0.query.filter_by(user=current_user.id).all()
    if form.validate_on_submit():
        spider_settings0 = SpiderSettings0(
            user=current_user.id,
            project_name=form.project_name.data,
            spider_name=form.spider_name.data,
            start_url=form.start_url.data,
            allowed_domains=form.allowed_domains.data,
            item_pipelines='MongoDB' if form.item_pipelines.data == 2 else 'Mysql',
            db_url=form.db_url.data,
            collection=form.collection.data,
            dynamic=form.dynamic.data,
        )
        db.session.add(spider_settings0)
        db.session.commit()
        return redirect(url_for('.index'))
    if form_rules.validate_on_submit():
        spider_rules0 = SpiderRules0(
            user=current_user.id,
            restrict_xpaths=transform(form_rules.restrict_xpaths.data),
            allow=transform(form_rules.allow.data),
            callback=form_rules.callback.data,
            follow=form_rules.follow.data,
        )
        db.session.add(spider_rules0)
        db.session.commit()
        return redirect(url_for('.index'))
    if form_items.validate_on_submit():
        method_map = {1: 'xpath', 2: 'css', 3: 'value', 4: 'attr'}
        spider_item0 = SpiderItem0(
            user=current_user.id,
            keyword=form_items.keyword.data,
            method=method_map[form_items.method.data],
            args=transform(form_items.args.data),
            re=transform(form_items.re.data)
        )
        db.session.add(spider_item0)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('add_project/add.html', form=form, form_rules=form_rules, form_items=form_items,
                           settings=settings, rules=rules, items=items)


@add_project_bp.route('/delete_settings')
@login_required
def delete_settings():
    settings = SpiderSettings0.query.filter_by(user=current_user.id)
    for i in settings:
        db.session.delete(i)
        db.session.commit()
    return redirect(url_for('.index'))


@add_project_bp.route('/delete_rules/<rule_id>')
@login_required
def delete_rules(rule_id):
    if rule_id:
        rule = SpiderRules0.query.filter_by(id=rule_id).first()
        db.session.delete(rule)
        db.session.commit()
    else:
        rules = SpiderRules0.query.filter_by(user=current_user.id)
        for i in rules:
            db.session.delete(i)
            db.session.commit()
    return redirect(url_for('.index'))


@add_project_bp.route('/delete_items/<item_id>')
@login_required
def delete_items(item_id):
    if item_id:
        item = SpiderItem0.query.filter_by(id=item_id).first()
        db.session.delete(item)
        db.session.commit()
    else:
        items = SpiderItem0.query.filter_by(user=current_user.id)
        for i in items:
            db.session.delete(i)
            db.session.commit()
    return redirect(url_for('.index'))


@add_project_bp.route('/delete_all_settings')
@login_required
def delete_all_settings():
    settings = SpiderSettings0.query.filter_by(user=current_user.id)
    for i in settings:
        db.session.delete(i)
    rules = SpiderRules0.query.filter_by(user=current_user.id)
    for i in rules:
        db.session.delete(i)
    items = SpiderItem0.query.filter_by(user=current_user.id)
    for i in items:
        db.session.delete(i)
    db.session.commit()
    return redirect(url_for('.index'))


@add_project_bp.route('/confirm_settings')
@login_required
def confirm_settings():
    spider_settings0 = SpiderSettings0.query.filter_by(user=current_user.id).first()
    if not spider_settings0:
        flash('Please add project setting', 'danger')
        return redirect(url_for('.index'))

    spider_rules0 = SpiderRules0.query.filter_by(user=current_user.id).all()

    spider_item0 = SpiderItem0.query.filter_by(user=current_user.id).all()
    if not spider_item0:
        flash('Have at least one item', 'danger')
        return redirect(url_for('.index'))

    server = Server.query.order_by(Server.project_num).first()

    project_spider = ProjectSpider(
        project_name=spider_settings0.project_name,
        spider_name=spider_settings0.spider_name,
        author_id=spider_settings0.user,
        server_id=server.id
    )
    db.session.add(project_spider)
    try:
        db.session.commit()
    except:
        flash('Project Name has been used. Please change another one', 'danger')  # 检查项目名唯一
        return redirect(url_for('.index'))
    project_id = ProjectSpider.query.filter_by(project_name=spider_settings0.project_name).first().id

    spider_settings = SpiderSettings(
        start_url=spider_settings0.start_url,
        allowed_domains=spider_settings0.allowed_domains,
        collection=spider_settings0.project_name,
        item_pipelines=spider_settings0.item_pipelines,
        db_url=spider_settings0.db_url,
        db_name=current_user.username,
        dynamic=spider_settings0.dynamic,
        projectSpider_id=project_id
    )
    db.session.add(spider_settings)
    db.session.commit()

    for rule in spider_rules0:
        locals()['rule_' + str(rule.id)] = SpiderRules(
            restrict_xpaths=rule.restrict_xpaths,
            allow=rule.allow,
            callback=rule.callback,
            follow=rule.follow,
            projectSpider_id=project_id,
        )
        db.session.add(locals()['rule_' + str(rule.id)])
    db.session.commit()

    for item in spider_item0:
        locals()['item_' + str(item.id)] = SpiderItem(
            keyword=item.keyword,
            method=item.method,
            args=item.args,
            re=item.re,
            projectSpider_id=project_id
        )
        db.session.add(locals()['item_' + str(item.id)])
    db.session.commit()

    # 把设置写入模板并且上传至scrapyd
    write_setting(project_id)

    flash('Add a project setting successful!', 'success')

    # 更新服务器数据
    server.add_project()

    # 删除临时表
    db.session.delete(spider_settings0)
    for i in spider_rules0:
        db.session.delete(i)
    for i in spider_item0:
        db.session.delete(i)
    db.session.commit()
    return redirect(url_for('.index'))


@add_project_bp.route('/edit')
@login_required
def edit():
    pass
    return redirect(url_for('.index'))


