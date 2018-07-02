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


@user.route('answers/<user_id>')
def answers(user_id):
    r"""
    用户回答页面
    :param user_id:
    :return:
    """
    return render_template('user/user-answer.html')


@user.route('questions/<user_id>')
def questions(user_id):
    r"""
    用户问题页面
    :param user_id:
    :return:
    """
    return render_template('user/user-question.html')


@user.route('articles/<user_id>')
def articles(user_id):
    r"""
    用户文章页面
    :param user_id:
    :return:
    """
    return render_template('user/user-article.html')


@user.route('favorites/<user_id>')
def favorites(user_id):
    r"""
    用户收藏页面
    :param user_id:
    :return:
    """
    return render_template('user/user-collection.html')


@user.route('followers/<user_id>')
def followers(user_id):
    r"""
    用户
    :param user_id:
    :return:
    """
    return render_template('user/user-concern-me.html')
