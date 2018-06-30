import flask
from flask import render_template, redirect, url_for, request, session, g, flash
from . import admin
from app.models import *
from app.exts import db

#跳转到文章管理界面,查询所有用户
@admin.route('/tag',methods=['GET','POST'])
def taglist():
    #父类的id
    categoryId = request.args.get("categoryId")
    print(categoryId)
    tags = Tag.query.filter_by(parentId = categoryId)
    return render_template('admin/admin-tag.html',tags = tags)

#处理删除单个请求
@admin.route('/tag/delete', methods=['POST'])
def deletetag():
    tagId = request.form['tagId']
    currentCategory = Tag.query.filter_by(tagId=tagId).first()
    db.session.delete(currentCategory)
    db.session.commit()
    return redirect(url_for('admin.taglist'))

#处理批量删除
@admin.route('/tag/batchdelete', methods=['POST'])
def batchdeletetag():
    tagIds = request.form['tagIds']
    tids = tagIds.split(',');
    for tid in tids:
        currentCategory = Tag.query.filter_by(tagId=int(tid)).first()
        print(currentCategory)
        db.session.delete(currentCategory)
        db.session.commit()
    return redirect(url_for('admin.taglist'))

