from flask import render_template, Blueprint

user = Blueprint('user', __name__)

from . import views