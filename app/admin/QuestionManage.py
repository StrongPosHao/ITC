import flask
from flask import render_template, redirect, url_for, request, session, g, flash
from . import admin
from app.models import *
from app.exts import db

#跳转到文章管理界面,查询所有用户
@admin.route('/question')
def questionlist():
    questions = db.session.query(Question, User).filter(Question.userId == User.id).all()
    return render_template('admin/admin-question.html',questions = questions)

#处理删除单个请求
@admin.route('/question/delete', methods=['POST'])
def deletequestion():
    questionId = request.form['questionId']
    currentQuestion = Question.query.filter_by(questionId=questionId).first()
    db.session.delete(currentQuestion)
    db.session.commit()
    return redirect(url_for('admin.questionlist'))

#处理批量删除
@admin.route('/question/batchdelete', methods=['POST'])
def batchdeletequestion():
    questionIds = request.form['questionIds']
    qids = questionIds.split(',');
    for qid in qids:
        currentQuestion = Question.query.filter_by(questionId=int(qid)).first()
        print(currentQuestion)
        db.session.delete(currentQuestion)
        db.session.commit()
    return redirect(url_for('admin.questionlist'))

