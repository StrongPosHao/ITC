from flask import render_template, redirect, url_for, request, session, g, flash
from . import auth
from sqlalchemy import or_
from app.models import *
from app.exts import db
from flask_login import logout_user, login_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    r"""
    用户登录页面
    :return: index or login
    """
    if request.method == 'GET':
        return render_template('auth/Login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter(or_(User.email == username, User.phone == username, User.username == username), User.password == password).first()

        if user:
            session['username'] = username
            session.permanent = True
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误，请检查您的输入后重试')
            return redirect(url_for(login))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    r"""
    用户注册页面
    :return:
    """
    if request.method == 'GET':
        return render_template('auth/Register.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if not (email and phone and username and password):
            return redirect(url_for('register'))
        user = User(username=username, email=email, phone=phone, password=password)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/forget-password')
def forget_password():
    return render_template('auth/Login.html')


# @auth.before_app_request
# def my_before_request():
#     r"""
#     请求上下文管理器
#     :return:
#     """
#     user = session.get('user')
#     admin = session.get('admin')
#     if user:
#         g.user = user
#     if admin:
#         g.admin = admin


@auth.context_processor
def my_context_processor():
    r"""
    上下文处理器->将用户设置为可以在所有模板中访问
    :return:
    """
    username = session.get('username')
    adminname = session.get('admin')
    if username:
        user = User.query.filter(User.username == username).first()
        g.user = user
        return {'user': user}
    elif adminname:
        admin = Admin.query.filter(Admin.adminName == adminname).first()
        g.admin = admin
        return {'admin': admin}





