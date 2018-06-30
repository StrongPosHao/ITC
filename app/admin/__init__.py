from flask import render_template, Blueprint

admin = Blueprint('admin', __name__)

from . import views
from . import UserManage
from . import ArticleCommentManage
from . import AnswerCommentManage
from . import ArticleManage
from . import QuestionManage
from . import AnswerManage
from . import categoryManage
from . import TagManage
from . import ArticleTagManage
from . import QuestionTagManage
