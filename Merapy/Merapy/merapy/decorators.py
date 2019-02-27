from functools import wraps

from flask import flash, url_for, redirect, abort
from flask_login import current_user


def admin_required(func):  # 权限修饰器
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return decorated_function
