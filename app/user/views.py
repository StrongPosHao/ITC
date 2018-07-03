from flask import render_template, request, jsonify
from flask_login import current_user

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
    usr = User.query.filter(User.id == user_id).first()
    return render_template('user/user-answer.html', user=usr)


@user.route('questions/<user_id>')
def questions(user_id):
    r"""
    用户问题页面
    :param user_id:
    :return:
    """
    usr = User.query.filter(User.id == user_id).first()
    return render_template('user/user-question.html', user=usr)


@user.route('articles/<user_id>')
def articles(user_id):
    r"""
    用户文章页面
    :param user_id:
    :return:
    """
    usr = User.query.filter(User.id == user_id).first()
    return render_template('user/user-article.html', user=usr)


@user.route('favorites/<user_id>')
def favorites(user_id):
    r"""
    用户收藏页面
    :param user_id:
    :return:
    """
    questions = current_user.favoriteQuestions.order_by(FavoriteQuestion.time.desc()).all()
    articles= current_user.favoriteArticles.order_by(FavoriteArticle.time.desc()).all()
    favorites_list = questions + articles
    favorites_list = sorted(favorites_list, key=lambda x: x.time)
    usr = User.query.filter(User.id == user_id).first()
    return render_template('user/user-collection.html', favorites=favorites_list, user=usr)


@user.route('followers/<user_id>')
def followers(user_id):
    r"""
    用户关注的用户
    :param user_id:
    :return:
    """
    usr = User.query.filter(User.id == user_id).first()
    return render_template('user/user-my-concern.html', user=usr)


@user.route('followed/<user_id>')
def followed(user_id):
    r"""
    关注用户的用户
    :param user_id:
    :return:
    """
    usr = User.query.filter(User.id == user_id).first()
    return render_template('user/user-concern-me.html', user=usr)


@user.route('/choose-tag', methods=['POST'])
def user_choose_tag():
    r"""
    用户选择标签
    :return:
    """
    user_id = request.form.get('userId')
    tag_id = request.form.get('tagId')
    is_choosed = request.form.get('iscollected')
    print(user_id)
    print(tag_id)
    print(is_choosed)
    if is_choosed == 'true':
        user_tag = UserTag(userId=user_id, tagId=tag_id, time=datetime.now())
        db.session.add(user_tag)
        db.session.commit()
    elif is_choosed == 'false':
        user_tag = UserTag.query.filter(UserTag.userId == user_id, UserTag.tagId == tag_id).first()
        db.session.delete(user_tag)
        db.session.commit()
    data = {'info': 'Succeed'}
    return jsonify(data)


@user.route('/add-tag')
def add_tag():
    r"""
    用户添加标签页面
    :return:
    """
    return render_template('tag/tag-index.html')