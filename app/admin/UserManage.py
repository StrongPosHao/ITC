import flask
from flask import render_template, redirect, url_for, request, session,json, g, flash
import math
from . import admin
from app.models import *
from app.exts import db

allpages =1
currentpage = 1
#跳转到用户管理界面,查询所有用户
@admin.route('/user')
def index():
    page_size = 10
    page_index = currentpage
    users = User.query.filter_by(permission=0).limit(page_size).offset((page_index-1)*page_size)
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

#获取总页数并返回
@admin.route('/user/gettotalpage', methods=['GET','POST'])
def gettotalpage():
    users = User.query.filter_by(permission=0).all()
    size = math.ceil(len(users) / 10)
    global allpages
    allpages = size
    dict1 = {}
    dict1['size'] = size
    return json.dumps(dict1,ensure_ascii=False)

#改变当前页
@admin.route('/user/changepage', methods=['GET','POST'])
def changepage():
    current = request.form['current']
    page_size = 10
    #page_index = int(current)
    global currentpage
    if (int(current) == -1):
        if(currentpage == allpages):
            currentpage = allpages
        else:
            currentpage = currentpage + 1
    elif(int(current) == -2):
        if (currentpage == 1):
            currentpage = 1
        else:
            currentpage = currentpage - 1
    else:
        currentpage = int(current)
    users = User.query.filter_by(permission=0).limit(page_size).offset((currentpage-1)*page_size)
    list = []
    dict = {}
    for i in users:
        dict[repr(i.id)] = i.as_dict()
        list.append(dict[repr(i.id)])
    return json.dumps(list, ensure_ascii=False)
