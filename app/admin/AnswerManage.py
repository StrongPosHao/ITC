import flask
from flask import render_template, redirect, url_for, request, session, g, flash
from . import admin
from app.models import *
from app.exts import db

#跳转到文章管理界面,查询所有用户
@admin.route('/answer')
def answerlist():
    answers = db.session.query(Answer, User).filter(Answer.userId == User.id).all()
    return render_template('admin/admin-answer.html',answers = answers)

#处理删除单个请求
@admin.route('/answer/delete', methods=['POST'])
def deleteanswer():
    answerId = request.form['answerId']
    currentAnswer = Answer.query.filter_by(answerId=answerId).first()
    db.session.delete(currentAnswer)
    db.session.commit()
    return redirect(url_for('admin.answerlist'))

#处理批量删除
@admin.route('/answer/batchdelete', methods=['POST'])
def batchdeleteanswer():
    answerIds = request.form['answerIds']
    aids = answerIds.split(',');
    for aid in aids:
        currentAnswer = Answer.query.filter_by(answerId=int(aid)).first()
        print(currentAnswer)
        db.session.delete(currentAnswer)
        db.session.commit()
    return redirect(url_for('admin.answerlist'))

