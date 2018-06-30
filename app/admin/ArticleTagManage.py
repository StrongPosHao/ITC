import flask
from flask import render_template, redirect, url_for, request, session, g, flash,json,jsonify
from . import admin
from app.models import *
from app.exts import db


#跳转到用户管理界面,查询所有用户
@admin.route('/articletag')
def listTagByArticleId():
    tags = Tag.query.all()
    dict = {}
    for i in tags:
        dict[repr(i.tagId)] = i.as_dict()
    return json.dumps(dict,ensure_ascii=False)