import flask
from flask import render_template, redirect, url_for, request, session, g, flash
from . import admin
from app.models import *
from app.exts import db


#跳转到用户管理界面,查询所有用户
@admin.route('/answercomment')
def sclist():
    comments = db.session.query(AnswerComment, User).filter(AnswerComment.userId == User.id).all()
    return render_template('admin/admin-answercomment.html',comments = comments)

#处理删除单个请求
@admin.route('/answercomment/delete', methods=['POST'])
def deletesc():
    commentId = request.form['commentId']
    print(commentId)
    currentComment = AnswerComment.query.filter_by(commentId=commentId).first()
    print(currentComment)
    db.session.delete(currentComment)
    db.session.commit()
    return redirect(url_for('admin.sclist'))

#处理批量删除
@admin.route('/answercomment/batchdelete', methods=['POST'])
def batchdeletesc():
    commentIds = request.form['commentIds']
    cids = commentIds.split(',');
    print(cids)
    for cid in cids:
        currentComment = AnswerComment.query.filter_by(commentId=int(cid)).first()
        print(currentComment)
        db.session.delete(currentComment)
        db.session.commit()
    return redirect(url_for('admin.sclist'))