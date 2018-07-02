from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.exts import db
from datetime import datetime
from flask_login import UserMixin
from app.exts import login_manager
from sqlalchemy.orm import class_mapper

from sqlalchemy.exc import IntegrityError
from random import seed, randint
import forgery_py


class Follow(db.Model):
    __tablename__ = 'Follow'
    followerId = db.Column(db.BigInteger, db.ForeignKey('User.id'), primary_key=True)
    followedId = db.Column(db.BigInteger, db.ForeignKey('User.id'), primary_key=True)
    followTime = db.Column(db.DateTime, default=datetime.now())


class UserTag(db.Model):
    __tablename__ = 'UserTag'
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id'), primary_key=True, nullable=False)
    tagId = db.Column(db.BigInteger, db.ForeignKey('Tag.tagId'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class ArticleTag(db.Model):
    __tablename__ = 'ArticleTag'
    articleId = db.Column(db.BigInteger, db.ForeignKey('Article.articleId'), primary_key=True, nullable=False)
    tagId = db.Column(db.BigInteger, db.ForeignKey('Tag.tagId'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, articleId, tagId, time):
        self.articleId = articleId
        self.tagId = tagId
        self.time = time

    # 将类转为字典，然后响应json
    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) \
                    for col in class_mapper(obj.__class__).mapped_table.c)


class QuestionTag(db.Model):
    __tablename__ = 'QuestionTag'
    questionId = db.Column(db.BigInteger, db.ForeignKey('Question.questionId'), primary_key=True, nullable=False)
    tagId = db.Column(db.BigInteger, db.ForeignKey('Tag.tagId'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, questionId, tagId, time):
        self.questionId = questionId
        self.tagId = tagId
        self.time = time

    # 将类转为字典，然后响应json
    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) \
                    for col in class_mapper(obj.__class__).mapped_table.c)


class FavoriteArticle(db.Model):
    __tablename__ = 'FavoriteArticle'
    articleId = db.Column(db.BigInteger, db.ForeignKey('Article.articleId'), primary_key=True, nullable=False)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class FavoriteQuestion(db.Model):
    __tablename__ = 'FavoriteQuestion'
    questionId = db.Column(db.BigInteger, db.ForeignKey('Question.questionId'), primary_key=True, nullable=False)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(20), nullable=False)
    email = db.Column(db.Unicode(64), nullable=False)
    phone = db.Column(db.CHAR(11), nullable=False)
    password = db.Column(db.Unicode(100), nullable=False)
    headImage = db.Column(db.Unicode(256), default='static/image/defaultImage.jpg', nullable=False)
    permission = db.Column(db.CHAR(1), default=0, nullable=False)
    introduction = db.Column(db.Text, default='这家伙很懒，什么也没有写~', nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    tags = db.relationship('UserTag', backref=db.backref('tags'), lazy='dynamic')
    articles = db.relationship('Article', backref=db.backref('articles'), lazy='dynamic')
    questions = db.relationship('Question', backref=db.backref('questions'), lazy='dynamic')
    drafts = db.relationship('Draft', backref=db.backref('drafts'), lazy='dynamic')
    user_answers = db.relationship('Answer', backref=db.backref('user_answers'), lazy='dynamic')
    followed = db.relationship('Follow', foreign_keys=[Follow.followerId],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.followedId],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    favoriteArticles = db.relationship('FavoriteArticle', backref=db.backref('articles'), lazy='dynamic')
    favoriteQuestions = db.relationship('FavoriteQuestion', backref=db.backref('questions'), lazy='dynamic')
    notifications = db.relationship('Notification', backref=db.backref('notifications'), lazy='dynamic')


    # 将类转为字典，然后响应json
    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) \
                    for col in class_mapper(obj.__class__).mapped_table.c)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        # db.session.commit()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    @staticmethod
    def generate_fake(count=100):
        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     phone="18787053797",
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     introduction=forgery_py.lorem_ipsum.sentence(),
                     confirmed=True)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.BigInteger, primary_key=True)
    adminName = db.Column(db.Unicode(20), nullable=False)
    email = db.Column(db.Unicode(64), nullable=False)
    phone = db.Column(db.CHAR(11), nullable=False)
    password = db.Column(db.Unicode(100), nullable=False)
    headImage = db.Column(db.Unicode(256), nullable=False)
    permission = db.Column(db.CHAR(1), nullable=False)


class Question(db.Model):
    __tablename__ = 'Question'
    questionId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id'))
    title = db.Column(db.Unicode(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publicTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    answers = db.relationship('Answer', backref=db.backref('answers'))
    tags = db.relationship('QuestionTag', backref=db.backref('tags'), lazy='dynamic')
    favoriteUsers = db.relationship('FavoriteQuestion', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        seed()
        user_count = User.query.count()
        for i in range(count):
            user = User.query.offset(randint(0, user_count - 1)).first()
            title = forgery_py.lorem_ipsum.sentence()
            if len(title) > 50:
                title = title[:20]
            question = Question(userId=user.id, title=title,
                                content=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                                publicTime=forgery_py.date.date(True))
            db.session.add(question)
            try:
                db.session.commit()
            except:
                db.session.rollback()

    def get_user(self):
        return User.query.filter(User.id == self.userId).first().username


class Answer(db.Model):
    __tablename__ = 'Answer'
    answerId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id'), nullable=False)
    questionId = db.Column(db.BigInteger, db.ForeignKey('Question.questionId'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    answerTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    answerComments = db.relationship('AnswerComment', backref=db.backref('comments'), lazy='dynamic')

    def get_user(self):
        return User.query.filter(User.id == self.userId).first().username


class Article(db.Model):
    __tablename__ = 'Article'
    articleId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id'), nullable=False)
    title = db.Column(db.Unicode(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publicTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    articleComments = db.relationship('ArticleComment', backref=db.backref('comments'), lazy='dynamic')
    tags = db.relationship('ArticleTag', backref=db.backref('tags'), lazy='dynamic')
    favoriteUsers = db.relationship('FavoriteArticle', backref=db.backref('favoriteUsers'), lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        seed()
        user_count = User.query.count()
        for i in range(count):
            user = User.query.offset(randint(0, user_count - 1)).first()
            title = forgery_py.lorem_ipsum.sentence()
            if len(title) > 50:
                title = title[:20]
            print(len(title))
            article = Article(userId=user.id, title=title,
                              content=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                              publicTime=forgery_py.date.date(True))
            db.session.add(article)
            try:
                db.session.commit()
            except:
                db.session.rollback()

    def get_user(self):
        return User.query.filter(User.id == self.userId).first().username

    def get_user_object(self):
        return User.query.filter(User.id == self.userId).first()

    def get_article_comments(self):
        return ArticleComment.query.filter(ArticleComment.articleId == self.articleId,
                                           ArticleComment.parentId == None).all()


class Draft(db.Model):
    __tablename__ = 'Draft'
    draftId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id'), nullable=False)
    title = db.Column(db.Unicode(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    saveTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class Tag(db.Model):
    __tablename__ = 'Tag'
    tagId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    parentId = db.Column(db.BigInteger, db.ForeignKey('Tag.tagId'), nullable=True)
    name = db.Column(db.Unicode(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    popularity = db.Column(db.Integer, default=0, nullable=False)
    tagUsers = db.relationship('UserTag', backref=db.backref('users'), lazy='dynamic')
    articles = db.relationship('ArticleTag', backref=db.backref('articles'), lazy='dynamic')
    problems = db.relationship('QuestionTag', backref=db.backref('problems'), lazy='dynamic')

    def __init__(self, parentId, name, description, popularity):
        self.parentId = parentId
        self.name = name
        self.description = description
        self.popularity = popularity

    # 将类转为字典，然后响应json
    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) \
                    for col in class_mapper(obj.__class__).mapped_table.c)


class ArticleComment(db.Model):
    __tablename__ = 'ArticleComment'
    commentId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id'), nullable=False)
    parentId = db.Column(db.BigInteger, db.ForeignKey('ArticleComment.commentId'), nullable=True)
    articleId = db.Column(db.BigInteger, db.ForeignKey('Article.articleId'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    commentTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # articleChildComments = db.relationship('ArticleComment', backref=db.backref('articleChildComments'))

    def get_user(self):
        return User.query.filter(User.id == self.userId).first().username

    def get_parent_comments(self):
        return ArticleComment.query.filter(ArticleComment.parentId is None).all()

    def get_child_comments(self):
        return ArticleComment.query.filter(ArticleComment.parentId == self.commentId).all()


class AnswerComment(db.Model):
    __tablename__ = 'AnswerComment'
    commentId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    parentId = db.Column(db.BigInteger, db.ForeignKey('AnswerComment.commentId'), nullable=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id'), nullable=False)
    answerId = db.Column(db.BigInteger, db.ForeignKey('Answer.answerId'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    commentTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # answerChildComments = db.relationship('AnswerComment', backref=db.backref('answerChildComments'))

    def get_user(self):
        return User.query.filter(User.id == self.userId).first().username


class Notification(db.Model):
    __tablename__ = 'Notification'
    notificationId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.Unicode(200), nullable=False)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    isRead = db.Column(db.Boolean, default=False, nullable=False)
    notifyTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
