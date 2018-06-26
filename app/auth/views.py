import flask
from flask import render_template, redirect, url_for, request, session, g, flash
from app.email import send_mail
from . import auth
from sqlalchemy import or_
from app.models import *
from app.exts import db
from flask_login import logout_user, login_required, login_user, current_user


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


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

        user = User.query.filter(or_(User.email == username, User.phone == username, User.username == username),
                                 User.password == password).first()

        if user:
            session['username'] = username
            # session.permanent = True
            login_user(user, remember=True)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('用户名或密码错误，请检查您的输入后重试')
            return redirect(url_for('auth.login'))


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
        if not (email and phone and username and password):
            return render_template('auth/Register.html')
        user = User(username=username, email=email, phone=phone, password=password)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        return '一封确认邮件已发往您的邮箱，请进入您的邮箱查看并确认以完成最后一步！'


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
    else:
        flash('确认链接无效或已过期！')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.mail, 'Confirm Your Account',
              'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    r"""
    忘记密码路由函数
    :param token:
    :return:
    """
    if request.method == 'GET':
        return render_template('auth/forget-password.html')
    else:
        if not current_user.is_anonymous:
            return redirect(url_for('main.index'))
        username = request.form.get('username')
        user = User.query.filter(User.username == username).first()
        if user is None:
            return '该用户不存在'
        email = request.form.get('email')
        phone = request.form.get('phone')
        if email != user.email or phone != user.phone:
            return '用户邮箱或手机号输入有误'
        token = user.generate_reset_token()
        send_mail(user.email, 'Reset Your Password', 'auth/email/reset_password' , user=user, token=token, next=request.args.get('next'))
        return '一封确认和指导您重置密码的邮件已发往您的邮箱中!'


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if request.method == 'GET':
        return render_template('auth/reset-password.html')
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    else:
        user = User.query.filter(User.email == request.form.get('email')).first()
        if user is None:
            return '邮箱输入错误'
        if user.reset_password(token, request.form.get('password')):
            db.session.commit()
            flash('密码重置成功！')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))



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
#
#
# @auth.context_processor
# def my_context_processor():
#     r"""
#     上下文处理器->将用户设置为可以在所有模板中访问
#     :return:
#     """
#     username = session.get('username')
#     adminname = session.get('admin')
#     if username:
#         user = User.query.filter(User.username == username).first()
#         g.user = user
#         return {'user': user}
#     elif adminname:
#         admin = Admin.query.filter(Admin.adminName == adminname).first()
#         g.admin = admin
#         return {'admin': admin}
#
