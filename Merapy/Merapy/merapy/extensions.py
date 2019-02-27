# -*-coding:utf-8-*-

from flask_bootstrap import Bootstrap
from flask_login import LoginManager, AnonymousUserMixin
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from scrapyd_api import ScrapydAPI

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
moment = Moment()
csrf = CSRFProtect()


# 登录管理，可以查询到当前登录用户的完整信息
@login_manager.user_loader
def load_user(user_id):
    from merapy.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.re_authenticate'
# login_manager.needs_refresh_message = 'Your custom message'
login_manager.needs_refresh_message_category = 'warning'


class Guest(AnonymousUserMixin):  # 游客类，对于未登录的用户需要增加的属性

    @property
    def is_admin(self):
        return False


login_manager.anonymous_user = Guest
