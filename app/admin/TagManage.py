import flask
from flask import render_template, redirect, url_for, request, session, g, flash
from . import admin
from app.models import *
from app.exts import db

cid = 0
#跳转到文章管理界面,查询所有用户
@admin.route('/tag',methods=['GET','POST'])
def taglist():
    #父类的id
    categoryId = request.args.get("categoryId")
    global cid
    cid = int(categoryId)
    print("cid:" + cid)
    tags = Tag.query.filter_by(parentId = categoryId)
    return render_template('admin/admin-tag.html',tags = tags)

#处理删除单个请求
@admin.route('/tag/delete', methods=['POST'])
def deletetag():
    tagId = request.form['tagId']
    currentTag = Tag.query.filter_by(tagId=tagId).first()
    db.session.delete(currentTag)
    db.session.commit()
    return redirect(url_for('admin.taglist'))

#处理批量删除
@admin.route('/tag/batchdelete', methods=['POST'])
def batchdeletetag():
    tagIds = request.form['tagIds']
    tids = tagIds.split(',');
    for tid in tids:
        currentTag = Tag.query.filter_by(tagId=int(tid)).first()
        db.session.delete(currentTag)
        db.session.commit()
    return redirect(url_for('admin.taglist'))

#处理新增
@admin.route('/tag/add', methods=['GET','POST'])
def AddTag():
    tagName = request.form['tagName']
    tagDescription = request.form['tagDescription']
    categoryId = request.args.get("categoryId")

    tag = Tag(cid,tagName,tagDescription,0)
    db.session.add(tag)
    db.session.commit()
    return redirect(url_for('admin.taglist'))

#处理编辑
@admin.route('/tag/edit', methods=['GET','POST'])
def editTag():
    tagId = request.form['tagId']
    tagName = request.form['tagName']
    tagDescription = request.form['tagDescription']

    currentTag = Tag.query.filter_by(tagId=int(tagId)).first()
    currentTag.name = tagName
    currentTag.description = tagDescription
    db.session.commit()

    return redirect(url_for('admin.taglist'))

