from flask import render_template
from . import main


@main.route('/')
def index():

    # return render_template('main/index.html')
    return render_template('auth/auth-info.html')

