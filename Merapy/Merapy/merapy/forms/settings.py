# -*-coding:utf-8-*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, URL

from merapy.models import User
from flask import current_app


class SpiderSettingsForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(1, 20), Regexp('^[a-zA-Z0-9_]*$',
                                                                                                 message='The username should contain only a-z, A-Z,0-9 and _.')],
                               description='')
    spider_name = StringField('Spider Name', validators=[Length(1, 20), Regexp('^[a-zA-Z0-9_]*$', message='The username should contain only a-z, A-Z,0-9 and _.')],
                              description='', default='spider')
    start_url = StringField('Start Url', validators=[DataRequired(), URL()],
                            description='')
    allowed_domains = StringField('Allowed Domains', validators=[DataRequired(), Length(1, 50), Regexp('^[a-zA-Z0-9\.:/]',message='Invalid URL')],
                                  description='')
    collection = StringField('Storage Space', validators=[Length(1, 50), Regexp('^[a-zA-Z0-9_]*$',
                                                                                                message='The username should contain only a-z, A-Z,0-9 and _.')],
                             description='', default='default')
    item_pipelines = RadioField('DB Type', choices=[(1,'Mysql'), (2,'MongoDB')], description='', coerce=int)

    db_url = StringField('DB Url', validators=[DataRequired(), Length(1, 60)], description='You can choose your own data source if you have', default='default')

    dynamic = BooleanField('Dynamic', description='is or not dynamic_web')

    submit1 = SubmitField('Add')


class SpiderRulesForm(FlaskForm):
    restrict_xpaths = StringField(render_kw={'class': 'form-control', 'placeholder': 'restrict_xpaths'}, validators=[DataRequired(message="111")])
    allow = StringField(render_kw={'class': 'form-control', 'placeholder': 'allow'}, )
    callback = BooleanField(description='Callback or No')
    follow = BooleanField(description='Follow or No')
    submit2 = SubmitField('Add')


class SpiderItemForm(FlaskForm):
    keyword = StringField(render_kw={'class': 'form-control', 'placeholder': 'keyword'}, validators=[DataRequired()])
    method = SelectField('Method', render_kw={'class': 'form-control m-b', 'placeholder': 'method'}, validators=[DataRequired()],
                         choices=[(1, 'xpath'), (2, 'css'), (3, 'value'), (4, 'attr')], coerce=int)
    args = StringField(render_kw={'class': 'form-control', 'placeholder': 'args'}, validators=[DataRequired()])
    re = StringField(render_kw={'class': 'form-control', 'placeholder': 're'}, )
    submit3 = SubmitField('Add')


