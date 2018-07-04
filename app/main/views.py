from flask import render_template, request
from . import main
from flask_login import login_required, current_user
from ..models import Article, Question, User
from sqlalchemy import or_
import jieba


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    tags = current_user.tags.all()
    questions = []
    articles = []
    for tag in map(lambda x: x.get_object(), tags):
        question = tag.problems.all()
        article = tag.articles.all()
        questions = list(set(questions + question))
        articles = list(set(articles + article))
    res = questions+articles
    return render_template('main/search.html', result=map(lambda x: x.get_item(), res))


@main.route('/test')
def test():
    # return render_template('tag/tag-index.html')
    return render_template('tag/tag-list.html')


@main.route('/search', methods=['GET', 'POST'])
def search():
    r"""
    搜索功能路由函数
    :return:
    """
    search_input = request.form.get('search-input')
    seg_list = jieba.cut_for_search(search_input)
    questions = []
    articles = []
    for seg in seg_list:
        question = Question.query.filter(or_(Question.title.contains(seg), Question.content.contains(seg))).all()
        article = Article.query.filter(or_(Article.title.contains(seg), Article.content.contains(seg))).all()
        questions = list(set(questions + question))
        articles = list(set(articles + article))
    questions.reverse()
    articles.reverse()
    result = questions + articles
    return render_template('main/search.html', result=result)
