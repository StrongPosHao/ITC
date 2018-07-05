from flask import render_template, request, redirect, url_for, current_app, json, jsonify
from . import article
from flask_login import current_user, login_required
from ..models import User, Article, ArticleTag, Tag, Draft, ArticleComment, FavoriteArticle, Follow, LikeArticle, \
    UnlikeArticle
from datetime import datetime
from app.exts import db


@article.route('/<article_id>', methods=['GET', 'POST'])
def content(article_id):
    r"""
    文章内容页面
    :return:
    """
    article1 = Article.query.filter(Article.articleId == article_id).first()
    is_follow = True if current_user.is_following(article1.get_user_object()) else False
    if request.method == 'GET':
        return render_template('article/article-content.html', article=article1, is_follow=is_follow)
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


@article.route('/after-comment/<article_id>/<parent_id>', methods=['POST'])
@login_required
def after_comment(article_id, parent_id):
    r"""
    用于发表追评的路由函数
    :return:
    """
    the_content = request.form.get('after-comment')
    the_comment = ArticleComment(parentId=parent_id, articleId=article_id, content=the_content,
                                 commentTime=datetime.now(),
                                 userId=current_user.id)
    db.session.add(the_comment)
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
    info = {'info': 'Succeed'}
    return jsonify(info)


@article.route('/like', methods=['POST'])
def like():
    r"""
    用于处理用户点赞的路由函数
    :return:
    """
    is_checked = request.form.get('ischecked')
    article_id = request.form.get('article_id')
    user_id = request.form.get('user_id')
    if is_checked == 'true':
        time = datetime.now()
        like_article = LikeArticle(articleId=article_id, userId=user_id, time=time)
        db.session.add(like_article)
        db.session.commit()
    elif is_checked == 'false':
        like_article = LikeArticle.query.filter(LikeArticle.articleId == article_id,
                                                LikeArticle.userId == user_id).first()
        db.session.delete(like_article)
        db.session.commit()
    info = {'info:' 'Succeed'}
    return jsonify(info)


@article.route('/unlike', methods=['POST'])
def unlike():
    r"""
    用于处理用户点踩的路由函数
    :return:
    """
    is_checked = request.form.get('ischecked')
    article_id = request.form.get('article_id')
    user_id = request.form.get('user_id')
    if is_checked == 'true':
        time = datetime.now()
        unlike_article = UnlikeArticle(articleId=article_id, userId=user_id, time=time)
        db.session.add(unlike_article)
        db.session.commit()
    elif is_checked == 'false':
        unlike_article = UnlikeArticle.query.filter(UnlikeArticle.articleId == article_id,
                                                    UnlikeArticle.userId == user_id).first()
        db.session.delete(unlike_article)
        db.session.commit()
    info = {'info': 'Succeed'}
    return jsonify(info)


@article.route('/delete-comment', methods=['POST'])
def delete_comment():
    r"""
    用于删除评论的路由函数
    :return:
    """
    comment_id = request.form.get('commentId')
    comment = ArticleComment.query.filter(ArticleComment.commentId == comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    info = {'info': 'Succeed'}
    return jsonify(info)


@article.route('/publish', methods=['GET', 'POST'])
def publish():
    r"""
    文章发表页面
    :return:
    """
    if request.method == 'GET':
        tags = Tag.query.filter(Tag.parentId != None).all()
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
            the_draft = Draft.query.filter(Draft.userId == user_id, Draft.title == title).first()
            info = {'info:': 'Succeed'}
            return redirect(url_for('article.draft', draft_id=the_draft.draftId, _external=True))


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


@article.route('/focus-author', methods=['POST'])
def focus_author():
    r"""
    关注作者处理函数
    :return:
    """
    follower_id = request.form.get('user_id')
    followed_id = request.form.get('writer_id')
    is_focused = request.form.get('ischecked')
    if is_focused == 'true':
        follow = Follow(followerId=follower_id, followedId=followed_id, followTime=datetime.now())
        db.session.add(follow)
        db.session.commit()
    elif is_focused == 'false':
        follow = Follow.query.filter(Follow.followerId == follower_id, Follow.followedId == followed_id).first()
        db.session.delete(follow)
        db.session.commit()
    data = {'info': 'Succeed'}
    return jsonify(data)


@article.route('/draft/<draft_id>', methods=['GET', 'POST'])
def draft(draft_id):
    r"""
    用户查看草稿页面
    :return:
    """
    this_draft = Draft.query.filter(Draft.draftId == draft_id).first()
    tags = Tag.query.filter(Tag.parentId != None).all()
    return render_template('article/article-publish.html', tags=tags, draft=this_draft)
