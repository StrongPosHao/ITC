from flask import render_template, request
from . import user
from .. models import *


@user.route('info/<user_id>')
def info(user_id):
    r"""
    用户个人信息页面
    :param user_id:
    :return:
    """
    usr = User.query.filter(User.id == user_id).first()
    if request.method == 'GET':
        return render_template('user/user-info.html', user=usr)


@user.route('notice/<user_id>')
def notification(user_id):
    r"""
    用户消息通知页面
    :param user_id:
    :return:
    """
    usr = User.query.filter(User.id == user_id).first()
    if request.method == 'GET':
        return render_template('user/user-notice.html', user=usr)


