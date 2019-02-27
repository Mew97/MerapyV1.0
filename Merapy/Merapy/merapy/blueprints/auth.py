from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login

from merapy.extensions import db
from merapy.forms.auth import LoginForm, RegisterForm, ChangePwdForm, VerifyUserForm
from merapy.models import User
from merapy.settings import Operations
from merapy.utils import redirect_back
from merapy import sms


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                # flash('Login success.', 'info')
                return redirect_back()
            else:
                flash('Your account is blocked.', 'warning')
                # return redirect(url_for('base.index'))
        flash('Invalid username or password.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('base.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))

    form = RegisterForm()

    if request.method == 'GET':
        phone_number = request.args.get('mobile_phone_number')
        if phone_number is not None:
            # pass
            if sms.send_message(phone_number):
                return render_template('auth/register.html', form=form)
            else:
                flash('Failed to get the verification code!', 'danger')
    elif form.validate_on_submit():  # 如果表格提交成功
        phone_number = request.form['phone']
        code = request.form['verification_code']
        if code == '':
            flash('Please input the verification code!', 'danger')
        elif sms.verify(phone_number, code):
            username = form.username.data
            password = form.password.data
            phone = form.phone.data
            user = User(
                username=username,
                phone=phone,
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Register successful!', 'success')
            return redirect(url_for('.login'))
        else:
            flash('Your code is wrong, please check again!', 'danger')
    return render_template('auth/register.html', form=form)


@auth_bp.route('/verify_user', methods=['GET', 'POST'])
def verify_user():
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))

    form = VerifyUserForm()

    if request.method == 'GET':
        phone_number = request.args.get('mobile_phone_number')
        if phone_number is not None:
            # pass
            if sms.send_message(phone_number):
                return render_template('auth/verify_user.html')
            else:
                flash('Failed to get the verification code!', 'danger')
    elif request.method == 'POST':
        phone_number = request.form['phone']
        user = User.query.filter_by(phone=phone_number).first()
        code = request.form['verification_code']
        if code == '':
            flash('Please input the verification code!', 'danger')
        elif sms.verify(phone_number, code):
        # elif code != '':
            login_user(user=user)
            return redirect(url_for('.change_pwd', user_id=user.id))
        else:
            flash('Verification code is error', 'danger')

    return render_template('auth/verify_user.html', form=form)


@auth_bp.route('/change_pwd/<user_id>', methods=['GET', 'POST'])
@login_required
def change_pwd(user_id):
    form = ChangePwdForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User.query.filter_by(id=user_id).first()
        user.set_password(password)
        db.session.commit()
        logout_user()
        return redirect(url_for('.login'))
    return render_template('auth/change_pwd.html', form=form)


