from flask import Flask, render_template
from config import Config
from .exts import db
from .exts import mail
from .models import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    db.init_app(app)

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
