import flask
from flask import render_template, redirect, url_for, request, session, g, flash
from . import admin
from app.models import *
from app.exts import db


#跳转到用户管理界面,查询所有用户
@admin.route('/articlecomment')
def aclist():
    #comments = ArticleComment.query.all()
    comments = db.session.query(ArticleComment, Article).filter(Article.articleId == ArticleComment.articleId).all()
    return render_template('admin/admin-articlecomment.html',comments = comments)

#处理删除单个请求
@admin.route('/articlecomment/delete', methods=['POST'])
def deleteac():
    commentId = request.form['commentId']
    currentComment = ArticleComment.query.filter_by(commentId=commentId).first()
    db.session.delete(currentComment)
    db.session.commit()
    return redirect(url_for('admin.aclist'))

#处理批量删除
@admin.route('/articlecomment/batchdelete', methods=['POST'])
def batchdeleteac():
    commentIds = request.form['commentIds']
    cids = commentIds.split(',');
    print(cids)
    for cid in cids:
        currentComment = ArticleComment.query.filter_by(commentId=int(cid)).first()
        print(currentComment)
        db.session.delete(currentComment)
        db.session.commit()
    return redirect(url_for('admin.aclist'))