from flask import render_template
from . import question


@question.route('/')
def content():
    return render_template('question/question-content.html')


@question.route('/publish')
def publish():
    return '发布问题'


@question.route('/list')
def list_question():
    return render_template('question/question-list.html')


