from flask import render_template, request, redirect, url_for, current_app
from . import article
from flask_login import current_user
from ..models import User, Article, ArticleTag, Tag, Draft
from datetime import datetime
from app.exts import db


@article.route('/<article_id>', methods=['GET', 'POST'])
def content(article_id):
    r"""
    文章内容页面
    :return:
    """
    if request.method == 'GET':
        return render_template('article/article-content.html')


@article.route('/publish', methods=['GET', 'POST'])
def publish():
    r"""
    文章发表页面
    :return:
    """
    if request.method == 'GET':
        return render_template('article/article-publish.html')
    else:
        user_id = current_user.id
        title = request.form.get('title')
        article_content = request.form.get('content')
        tag_name = request.form.get('tag')
        public_time = datetime.now()
        if request.form.get('publish', None) == '发表':
            article = Article(userId=user_id, title=title, content=article_content, publicTime=public_time)
            db.session.add(article)
            db.session.commit()
            tag = Tag.query.filter(Tag.name == tag_name).first()
            article_tag = ArticleTag(articleId=article.articleId, tagId=tag.tagId, time=datetime.now())
            db.session.add(article_tag)
            db.session.commit()
            return redirect(url_for('article.list_article'))
        elif request.form.get('save', None) == '草稿':
            draft = Draft(userId=user_id, title=title, content=article_content, saveTime=public_time)
            db.session.add(draft)
            db.session.commit()
            return '草稿保存成功'


@article.route('/list')
def list_article():
    """
    文章列表页面
    :return:
    """
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.publicTime.desc()).paginate(
        page, per_page=current_app.config['ITC_PER_PAGE'],
        error_out=False
    )
    articles = pagination.items
    return render_template('article/article-list.html', articles=articles, pagination=pagination)
