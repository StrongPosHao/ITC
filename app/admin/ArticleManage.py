import flask
from flask import render_template, redirect, url_for, request, session, g, flash
from . import admin
from app.models import *
from app.exts import db

#跳转到文章管理界面,查询所有用户
@admin.route('/article')
def articlelist():
    articles = db.session.query(Article, User).filter(Article.userId == User.id).all()
    return render_template('admin/admin-article.html',articles = articles)

#处理删除单个请求
@admin.route('/article/delete', methods=['POST'])
def deletearticle():
    articleId = request.form['articleId']
    currentArticle = Article.query.filter_by(articleId=articleId).first()
    db.session.delete(currentArticle)
    db.session.commit()
    return redirect(url_for('admin.articlelist'))

#处理批量删除
@admin.route('/article/batchdelete', methods=['POST'])
def batchdeletearticle():
    articleIds = request.form['articleIds']
    aids = articleIds.split(',');
    for aid in aids:
        currentArticle = Article.query.filter_by(articleId=int(aid)).first()
        print(currentArticle)
        db.session.delete(currentArticle)
        db.session.commit()
    return redirect(url_for('admin.articlelist'))

