from flask import render_template, request, current_app, redirect, url_for, jsonify
from . import question
from ..models import Question, User, Answer, AnswerComment, QuestionTag, FavoriteQuestion, LikeAnswer, UnlikeAnswer
from ..exts import db
from datetime import datetime
from flask_login import current_user, login_required
import json


@question.route('/<question_id>', methods=['GET', 'POST'])
def content(question_id):
    ques = Question.query.filter(Question.questionId == question_id).first()
    answers = ques.answers.all()
    answer_comments_list = []
    for answer in answers:
        answer_comments = answer.answerComments
        answer_comments_list.append(answer_comments)
    if request.method == 'GET':
        return render_template('question/question-content.html', question=ques, question_id=question_id,
                               answers=answers, answer_comments_list=answer_comments_list)
    else:
        if request.form.get('answer', None) == 'answer':
            answer_content = request.form.get('answer_content')
            user_id = current_user.id
            title = ques.title
            answer_time = datetime.now()
            answer = Answer(userId=user_id, questionId=question_id, content=answer_content,
                            answerTime=answer_time)
            db.session.add(answer)
            db.session.commit()
        return redirect(url_for('question.content', question_id=question_id, _external=True))


@question.route('/comment_answer', methods=['POST'])
@login_required
def comment_answer():
    data = json.loads(request.form.get('data'))
    user_id = current_user.id
    comment_content = data['content']
    answer_id = data['answerId']
    comment_time = datetime.now()
    question_id = data['questionId']
    answer_comment = AnswerComment(userId=user_id, content=comment_content, answerId=answer_id,
                                   commentTime=comment_time)
    db.session.add(answer_comment)
    db.session.commit()
    return redirect(url_for('question.content', question_id=question_id, _external=True))


@question.route('/delete-comment', methods=['POST'])
@login_required
def delete_comment():
    comment_id = request.form.get('commentId')
    print(comment_id)
    comment = AnswerComment.query.filter(AnswerComment.commentId == comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    info = {'info': 'Succeed'}
    return jsonify(info)


@question.route('/delete-answer', methods=['POST'])
def delete_answer():
    answer_id = request.form.get('answerId')
    answer = Answer.query.filter(Answer.answerId == answer_id).first()
    db.session.delete(answer)
    db.session.commit()
    info = {'info': 'Succeed'}
    return jsonify(info)


@question.route('/list')
def list_question():
    r"""
    问题列表页面
    :return:
    """
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by(Question.publicTime.desc()).paginate(
        page, per_page=current_app.config['ITC_PER_PAGE'],
        error_out=False
    )
    questions = pagination.items
    return render_template('question/question-list.html', questions=questions, pagination=pagination)


@question.route('/list/<user_id>')
def list_user_question(user_id):
    r"""
    用户问题列表页面
    :param user_id:
    :return:
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter(User.id == user_id).first()
    pagination = user.questions.paginate(page, per_page=current_app.config['ITC_PER_PAGE'], error_out=False)
    questions = pagination.items
    return render_template('question/question-list.html', questions=questions, pagination=pagination)


@question.route('/publish-question', methods=['POST'])
@login_required
def publish_question():
    r"""
    发表问题
    :return:
    """
    user_id = current_user.id
    title = request.form['question_title']
    ques_content = request.form['questionEditor']
    tag_id = request.form['tag_id']
    public_time = datetime.now()
    ques = Question(userId=user_id, title=title, content=ques_content, publicTime=public_time)
    db.session.add(ques)
    db.session.commit()
    this_question = Question.query.filter(Question.userId == user_id, Question.title == title).first()
    ques_tag = QuestionTag(questionId=this_question.questionId, tagId=tag_id, time=datetime.now())
    db.session.add(ques_tag)
    db.session.commit()
    return redirect(url_for('question.content', question_id=this_question.questionId, _external=True))


@question.route('/favorite', methods=['POST'])
@login_required
def favorite_question():
    r"""
    收藏问题
    :return:
    """
    is_checked = request.form.get('ischecked')
    question_id = request.form.get('problemId')
    user_id = request.form.get('userId')
    if is_checked == 'true':
        time = datetime.now()
        favorite_question = FavoriteQuestion(questionId=question_id, userId=user_id, time=time)
        db.session.add(favorite_question)
        db.session.commit()
    elif is_checked == 'false':
        favorite_question = FavoriteQuestion.query.filter(FavoriteQuestion.questionId == question_id,
                                                          FavoriteQuestion.userId == user_id).first()
        db.session.add(favorite_question)
        db.session.commit()
    info = {'info': 'Succeed'}
    return jsonify(info)


@question.route('/after-comment/<question_id>/<answer_id>/<parent_id>', methods=['POST'])
@login_required
def after_comment(question_id, answer_id, parent_id):
    r"""
    追评处理路由函数
    :return:
    """
    the_content = request.form.get('after-comment')
    answer_comment = AnswerComment(parentId=parent_id, userId=current_user.id, content=the_content,
                                   commentTime=datetime.now(), answerId=answer_id)
    db.session.add(answer_comment)
    db.session.commit()
    return redirect(url_for('question.content', question_id=question_id))


@question.route('/like-answer', methods=['POST'])
@login_required
def like_answer():
    r"""
    用户对回答点赞操作
    :return:
    """
    user_id = request.form.get('userId')
    answer_id = request.form.get('answerId')
    like = LikeAnswer(userId=user_id, answerId=answer_id, time=datetime.now())
    db.session.add(like)
    db.session.commit()
    info = {'info': 'Succeed'}
    return jsonify(info)


@question.route('/unlike-answer', methods=['POST'])
@login_required
def unlike_answer():
    r"""
    用户对回答点踩操作
    :return:
    """
    user_id = request.form.get('userId')
    answer_id = request.form.get('answerId')
    unlike = UnlikeAnswer(userId=user_id, answerId=answer_id, time=datetime.now())
    db.session.add(unlike)
    db.session.commit()
    info = {'info': 'Succeed'}
    return jsonify(info)
