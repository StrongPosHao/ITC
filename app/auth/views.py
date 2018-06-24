from flask import render_template, redirect, url_for, request, session, g, flash
from . import auth
from sqlalchemy import or_
from app.models import *
from app.exts import db


# @auth.app_context_processor()
# def


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

        user = User.query.filter(or_(User.email == username, User.phone == username, User.userName == username), User.password == password).first()

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
        print(user)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/forget-password')
def forget_password():
    return render_template('auth/Login.html')




