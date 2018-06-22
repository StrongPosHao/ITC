from flask import render_template, Blueprint

question = Blueprint('question', __name__)

from . import views