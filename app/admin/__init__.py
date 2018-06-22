from flask import render_template, Blueprint

admin = Blueprint('admin', __name__)

from . import views


