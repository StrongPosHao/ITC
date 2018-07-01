import flask
from flask import render_template, redirect, url_for, request, session, g, flash,json,jsonify
from . import admin
from app.models import *
from app.exts import db
from datetime import datetime


#根据文章的id查询所有已分配的标签
@admin.route('/questiontag', methods=['GET','POST'])
def listTagByQuestionId():
    questionId = request.form['questionId']
    #tags = QuestionTag.query.filter_by(questionId=questionId)
    res = db.session.query(Tag,QuestionTag).filter(QuestionTag.questionId==questionId,QuestionTag.tagId==Tag.tagId).all()
    tags = []
    for ele in res:
        tags.append(ele[0])
    list = []
    dict = {}
    for i in tags:
        dict[repr(i.tagId)] = i.as_dict()
        list.append(dict[repr(i.tagId)])
    return json.dumps(list,ensure_ascii=False)

#查询所有的子标签
@admin.route('/questiontag/all', methods=['GET','POST'])
def listAllQuestionTag():
    tags = Tag.query.filter(Tag.parentId != None).all()
    list = []
    dict = {}
    for i in tags:
        dict[repr(i.tagId)] = i.as_dict()
        list.append(dict[repr(i.tagId)])
    return json.dumps(list,ensure_ascii=False)

#向数据库发sql修改文章的标签
@admin.route('/questiontag/changetag', methods=['GET','POST'])
def changeuestiontag():
    tagIds = request.form['tagIds']
    questionId = request.form['questionId']
    qids = tagIds.split(",")
    #首先查询之前的标签文章删除
    questions = QuestionTag.query.filter_by(questionId=int(questionId)).all()
    for question in questions:
        db.session.delete(question)
        db.session.commit()
    #然后在文章标签表中插入更改后的记录
    for qid in qids:
        at = QuestionTag(int(questionId),int(qid),datetime.now())
        db.session.add(at)
        db.session.commit()
    return redirect(url_for('admin.questionlist'))