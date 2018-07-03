from flask import render_template, request, redirect, url_for, current_app, json, jsonify
from . import article
from flask_login import current_user
from ..models import User, Article, ArticleTag, Tag, Draft, ArticleComment, FavoriteArticle
from datetime import datetime
from app.exts import db


@article.route('/<article_id>', methods=['GET', 'POST'])
def content(article_id):
    r"""
    文章内容页面
    :return:
    """
    article1 = Article.query.filter(Article.articleId == article_id).first()
    if request.method == 'GET':
        return render_template('article/article-content.html', article=article1)
    else:
        comment_content = request.form.get('comment_area')
        comment_time = datetime.now()
        article_comment = ArticleComment(articleId=article_id, content=comment_content, commentTime=comment_time,
                                         userId=current_user.id)
        db.session.add(article_comment)
        db.session.commit()
        return redirect(url_for('article.content', article_id=article_id, _external=True))


@article.route('/comment', methods=['POST'])
def comment():
    r"""
    用于发表评论的路由函数
    :return:
    """
    data = json.loads(request.form.get('data'))
    user_id = current_user.id
    comment_content = data['content']
    article_id = data['articleId']
    comment_time = datetime.now()
    parent_id = data['parentId']
    article_comment = ArticleComment(parentId=parent_id, articleId=article_id, content=comment_content,
                                     commentTime=comment_time, userId=user_id)
    db.session.add(article_comment)
    db.session.commit()
    return redirect(url_for('article.content', article_id=article_id, _external=True))


@article.route('/favorite', methods=['POST'])
def favorite():
    r"""
    用户收藏文章处理
    :return:
    """
    is_checked = request.form.get('ischecked')
    article_id = request.form.get('article_id')
    user_id = request.form.get('user_id')
    if is_checked == 'true':
        time = datetime.now()
        favorite_article = FavoriteArticle(articleId=article_id, userId=user_id, time=time)
        db.session.add(favorite_article)
        db.session.commit()
    elif is_checked == 'false':
        favorite_article = FavoriteArticle.query.filter(FavoriteArticle.articleId == article_id,
                                                        FavoriteArticle.userId == user_id).first()
        db.session.delete(favorite_article)
        db.session.commit()
    current_article = Article.query.filter(Article.articleId == article_id).first()
    data = {'favorite_user_num': len(current_article.favoriteUsers.all())}
    return jsonify(data)
    # return redirect(url_for('article.content', article_id=article_id, _external=True))


@article.route('/delete/<comment_id>', methods=['GET', 'POST'])
def delete(comment_id):
    r"""
    用于删除评论的路由函数
    :return:
    """
    article_comment = ArticleComment.query.filter(ArticleComment.commentId == comment_id).first()
    if not article_comment.parentId:
        child_comments = article_comment.get_child_comments()
        for child_comment in child_comments:
            db.session.delete(child_comment)
            db.session.commit()
    db.session.delete(article_comment)
    db.session.commit()
    return redirect(url_for('article.content', article_id=article_comment.articleId, _external=True))


@article.route('/publish', methods=['GET', 'POST'])
def publish():
    r"""
    文章发表页面
    :return:
    """
    if request.method == 'GET':
        tags = Tag.query.filter(Tag.parentId == None).all()
        return render_template('article/article-publish.html', tags=tags)
    else:
        user_id = current_user.id
        title = request.form.get('title')
        article_content = request.form.get('content')
        tag_id = request.form.get('tag')
        public_time = datetime.now()
        if request.form.get('publish', None) == '发表':
            article = Article(userId=user_id, title=title, content=article_content, publicTime=public_time)
            db.session.add(article)
            db.session.commit()
            article_tag = ArticleTag(articleId=article.articleId, tagId=tag_id, time=datetime.now())
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


@article.route('/list/<user_id>')
def list_user_article(user_id):
    r"""
    用户文章列表页面
    :return:
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter(User.id == user_id).first()
    pagination = user.articles.paginate(page, per_page=current_app.config['ITC_PER_PAGE'], error_out=False)
    articles = pagination.items
    return render_template('article/article-list.html', articles=articles, pagination=pagination)
