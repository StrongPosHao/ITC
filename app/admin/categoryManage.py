import flask
from flask import render_template, redirect, url_for, request, session, g, flash
from . import admin
from app.models import *
from app.exts import db

#跳转到文章管理界面,查询所有用户
@admin.route('/category')
def categorylist():
    #categorys = Tag.query.all()
    #找寻tag表中的所有父标签
    categorys = Tag.query.filter(Tag.parentId == None).all()
    return render_template('admin/admin-category.html',categorys = categorys)

#处理删除单个请求
@admin.route('/category/delete', methods=['POST'])
def deletecategory():
    categoryId = request.form['categoryId']
    currentCategory = Tag.query.filter_by(tagId=categoryId).first()
    db.session.delete(currentCategory)
    db.session.commit()
    return redirect(url_for('admin.categorylist'))

#处理批量删除
@admin.route('/category/batchdelete', methods=['POST'])
def batchdeletecategory():
    categoryIds = request.form['categoryIds']
    cids = categoryIds.split(',');
    for cid in cids:
        currentCategory = Tag.query.filter_by(tagId=int(cid)).first()
        print(currentCategory)
        db.session.delete(currentCategory)
        db.session.commit()
    return redirect(url_for('admin.categorylist'))

#处理新增
@admin.route('/category/add', methods=['GET','POST'])
def AddCategory():
    categoryName = request.form['categoryName']
    categoryDescription = request.form['categoryDescription']
    print(categoryName)
    print(categoryDescription)
    category = Tag(None,categoryName,categoryDescription,0)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('admin.categorylist'))

#处理编辑
@admin.route('/category/edit', methods=['GET','POST'])
def editCategory():
    categoryId = request.form['categoryId']
    categoryName = request.form['categoryName']
    categoryDescription = request.form['categoryDescription']

    currentCategory = Tag.query.filter_by(tagId=int(categoryId)).first()
    currentCategory.name = categoryName
    currentCategory.description = categoryDescription
    db.session.commit()

    return redirect(url_for('admin.categorylist'))