from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Regexp


class ServiceForm(FlaskForm):
    server_name = StringField('Server Name', validators=[DataRequired(), Length(1, 20), Regexp('^[a-zA-Z0-9_]*$',
                                                                                               message='The username should contain only a-z, A-Z,0-9 and _.')],description='')
    server_ip = StringField('Server IP', validators=[DataRequired(), Length(1, 20),
                                                     Regexp('^[0-9\.]*$', message='The Server IP is invalid'), ], description='')
    scrapyd_port = StringField('Scrapyd Port', validators=[DataRequired(), Length(1, 5), Regexp('^[0-9]*$',
                                                                                                message='The Server IP is invalid'), ], description='')
    username = StringField('Username', validators=[DataRequired()], description='')

    password = PasswordField('Password', validators=[DataRequired()], description='')

    submit = SubmitField('Add')
