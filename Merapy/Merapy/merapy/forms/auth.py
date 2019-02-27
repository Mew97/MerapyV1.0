from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Regexp

from merapy.models import User
from flask import current_app


class RegisterForm(FlaskForm):  # 注册表单类
    username = StringField(render_kw={'class': 'form-control', 'placeholder': 'Username'},
                           validators=[DataRequired(), Length(1, 20),
                                       Regexp('^[a-zA-Z0-9]*$',
                                              message='The username should contain only a-z, A-Z and 0-9.')])
    phone = StringField(render_kw={'class': 'form-control', 'placeholder': 'Phone Number', 'id': 'phone'},
                        validators=[DataRequired(), Length(11), Regexp('^[0-9]*$', message='The phone number should contain only 0-9')])
    verification_code = StringField(validators=[DataRequired()])
    password = PasswordField(render_kw={'class': 'form-control', 'placeholder': 'Password'}, validators=[
        DataRequired(), Length(6, 32)])
    password2 = PasswordField(render_kw={'class': 'form-control', 'placeholder': 'Confirm password'},
                              validators=[DataRequired(), EqualTo('password')])
    # invitationCode = StringField(render_kw={'class': 'form-control', 'placeholder': 'Invitation Code'},
    #                              validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField('Register', render_kw={'class': 'btn btn-success block full-width m-b'})

    # def validate_invitationCode(self, field):  # 验证邀请码
    #     if field.data != current_app.config['MERAPY_INVITATIONCODE']:
    #         raise ValidationError('The invitation code is invalid.')

    def validate_username(self, field):  # 验证用户名是否可用
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in use.')


class LoginForm(FlaskForm):  # 登陆表单类
    username = StringField(render_kw={'placeholder': 'Username', 'class': 'form-control'},
                           validators=[DataRequired(), Length(1, 254), Length(1, 20),
                                       Regexp('^[a-zA-Z0-9]*$',
                                              message='The username should contain only a-z, A-Z and 0-9.')])
    password = PasswordField(render_kw={'placeholder': 'Password', 'class': 'form-control'},
                             validators=[DataRequired()])
    remember_me = BooleanField('Remember me', render_kw={'type': 'checkbox'})
    submit = SubmitField('Log in', render_kw={'class': 'btn btn-success block full-width m-b'})


class ChangePwdForm(FlaskForm):
    password = PasswordField(render_kw={'class': 'form-control', 'placeholder': 'New Password'}, validators=[
        DataRequired(), Length(6, 32)])
    password2 = PasswordField(render_kw={'class': 'form-control', 'placeholder': 'Confirm password'},
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Confirm the changes', render_kw={'class': 'btn btn-success block full-width m-b'})


class VerifyUserForm(FlaskForm):
    username = StringField(render_kw={'placeholder': 'Username', 'class': 'form-control'},
                           validators=[DataRequired(), Length(1, 254), Length(1, 20),
                                       Regexp('^[a-zA-Z0-9]*$',
                                              message='The username should contain only a-z, A-Z and 0-9.')])
    phone = StringField(render_kw={'class': 'form-control', 'placeholder': 'Phone Number', 'id': 'phone'},
                        validators=[DataRequired(), Length(11),
                                    Regexp('^[0-9]*$', message='The phone number should contain only 0-9')])
    verification_code = StringField(validators=[DataRequired()])

