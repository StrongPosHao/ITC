from flask import Flask, render_template
from config import Config
from .exts import db
from .exts import mail
from .exts import login_manager
from .models import *
from flask_login import LoginManager


def create_app():
    r"""
    app的构造工厂函数。
    包括app的初始化配置和Blueprint的注册
    :return: app
    """

    # 初始化并加载配置
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Blueprint注册
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .article import article as article_blueprint
    app.register_blueprint(article_blueprint, url_prefix='/article')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .question import question as question_blueprint
    app.register_blueprint(question_blueprint, url_prefix='question')

    return app
