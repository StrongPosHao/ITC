import flask
from flask import render_template, redirect, url_for, request, session, g, flash
from . import admin
from app.models import *
from app.exts import db


#跳转到用户管理界面,查询所有用户
@admin.route('/user')
def index():
    users = Comm.query.filter_by(permission=0)
    return render_template('admin/admin-user.html',users = users)

#处理删除单个请求
@admin.route('/user/delete', methods=['POST'])
def delete():
    userId = request.form['userId']
    currentUser = User.query.filter_by(id=userId).first()
    db.session.delete(currentUser)
    db.session.commit()
    return redirect(url_for('admin.index'))

#处理批量删除
@admin.route('/user/batchdelete', methods=['POST'])
def batchdelete():
    userIds = request.form['userIds']
    uids = userIds.split(',');
    print(uids)
    for uid in uids:
        currentUser = User.query.filter_by(id=int(uid)).first()
        print(currentUser)
        db.session.delete(currentUser)
        db.session.commit()
    return redirect(url_for('admin.index'))