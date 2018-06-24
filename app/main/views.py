from flask import render_template
from . import main
from flask_login import login_required


@main.route('/')
@login_required
def index():
    # return render_template('main/index.html')
    return render_template('auth/auth-my-concern.html')