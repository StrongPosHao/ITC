import hashlib

from flask import current_app, request
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
    followerId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
    followedId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
    followTime = db.Column(db.DateTime, default=datetime.now())


class UserTag(db.Model):
    __tablename__ = 'UserTag'
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    tagId = db.Column(db.BigInteger, db.ForeignKey('Tag.tagId', ondelete='CASCADE'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def get_object(self):
        return Tag.query.filter(Tag.tagId == self.tagId).first()


class ArticleTag(db.Model):
    __tablename__ = 'ArticleTag'
    articleId = db.Column(db.BigInteger, db.ForeignKey('Article.articleId', ondelete='CASCADE'), primary_key=True,
                          nullable=False)
    tagId = db.Column(db.BigInteger, db.ForeignKey('Tag.tagId', ondelete='CASCADE'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, articleId, tagId, time):
        self.articleId = articleId
        self.tagId = tagId
        self.time = time

    # 将类转为字典，然后响应json
    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) \
                    for col in class_mapper(obj.__class__).mapped_table.c)

    def get_object(self):
        return Tag.query.filter(Tag.tagId == self.tagId).first()

    def get_item(self):
        return Article.query.filter(Article.articleId == self.articleId).first()


class QuestionTag(db.Model):
    __tablename__ = 'QuestionTag'
    questionId = db.Column(db.BigInteger, db.ForeignKey('Question.questionId', ondelete='CASCADE'), primary_key=True,
                           nullable=False)
    tagId = db.Column(db.BigInteger, db.ForeignKey('Tag.tagId', ondelete='CASCADE'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, questionId, tagId, time):
        self.questionId = questionId
        self.tagId = tagId
        self.time = time

    # 将类转为字典，然后响应json
    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) \
                    for col in class_mapper(obj.__class__).mapped_table.c)

    def get_object(self):
        return Tag.query.filter(Tag.tagId == self.tagId).first()

    def get_item(self):
        return Question.query.filter(Question.questionId == self.questionId).first()


class FavoriteArticle(db.Model):
    __tablename__ = 'FavoriteArticle'
    articleId = db.Column(db.BigInteger, db.ForeignKey('Article.articleId', ondelete='CASCADE'), primary_key=True,
                          nullable=False)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def get_object(self):
        return Article.query.filter(Article.articleId == self.articleId).first()


class FavoriteQuestion(db.Model):
    __tablename__ = 'FavoriteQuestion'
    questionId = db.Column(db.BigInteger, db.ForeignKey('Question.questionId', ondelete='CASCADE'), primary_key=True,
                           nullable=False)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def get_object(self):
        return Question.query.filter(Question.questionId == self.questionId).first()


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(20), nullable=False)
    email = db.Column(db.Unicode(64), nullable=False)
    phone = db.Column(db.CHAR(11), nullable=False)
    password = db.Column(db.Unicode(100), nullable=False)
    # headImage = db.Column(db.Unicode(256), default='static/image/defaultImage.jpg', nullable=False)
    avatar_hash = db.Column(db.String(32))
    permission = db.Column(db.CHAR(1), default=0, nullable=False)
    introduction = db.Column(db.Text, default='这家伙很懒，什么也没有写~', nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    tags = db.relationship('UserTag', backref=db.backref('tags'), lazy='dynamic', cascade='all, delete-orphan')
    articles = db.relationship('Article', backref=db.backref('articles'), lazy='dynamic', cascade='all, delete-orphan')
    questions = db.relationship('Question', backref=db.backref('questions'), lazy='dynamic',
                                cascade='all, delete-orphan')
    drafts = db.relationship('Draft', backref=db.backref('drafts'), lazy='dynamic', cascade='all, delete-orphan')
    user_answers = db.relationship('Answer', backref=db.backref('user_answers'), lazy='dynamic',
                                   cascade='all, delete-orphan')
    followed = db.relationship('Follow', foreign_keys=[Follow.followerId],  # 用户关注的用户: user.followed
                               backref=db.backref('follower', lazy='joined'),  # 关注用户的用户: user.follower
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.followedId],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    favoriteArticles = db.relationship('FavoriteArticle', backref=db.backref('favorite_articles'), lazy='dynamic',
                                       cascade='all, delete-orphan')
    favoriteQuestions = db.relationship('FavoriteQuestion', backref=db.backref('favorite_questions'), lazy='dynamic',
                                        cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref=db.backref('notifications'), lazy='dynamic',
                                    cascade='all, delete-orphan')
    likeArticles = db.relationship('LikeArticle', backref=db.backref('likeArticles'), lazy='dynamic',
                                   cascade='all, delete-orphan')
    likeAnswers = db.relationship('LikeAnswer', backref=db.backref('likeAnswers'), lazy='dynamic',
                                  cascade='all, delete-orphan')
    unlikeArticles = db.relationship('UnlikeArticle', backref=db.backref('unlikeArticles'), lazy='dynamic',
                                     cascade='all, delete-orphan')
    unlikeAnswers = db.relationship('UnlikeAnswer', backref=db.backref('unlikeAnswers'), lazy='dynamic',
                                    cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

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

    def is_following(self, user):
        return self.followed.filter_by(followedId=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(followerId=user.id).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(followerId=self.id, followedId=user.id)
            db.session.add(f)
            db.session.commit()

    def unfollow(self, user):
        f = self.followed.filter_by(followedId=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    def get_all_tags(self):
        return Tag.query.filter(Tag.parentId != None).all()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


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
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'))
    title = db.Column(db.Unicode(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publicTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    answers = db.relationship('Answer', backref=db.backref('answers'), lazy='dynamic', cascade='all, delete-orphan')
    tags = db.relationship('QuestionTag', backref=db.backref('tags'), lazy='dynamic', cascade='all, delete-orphan')
    favoriteUsers = db.relationship('FavoriteQuestion', backref=db.backref('favorite_users'), lazy='dynamic',
                                    cascade='all, delete-orphan')

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

    def is_user_favorite(self, user):
        return 'true' if self.questionId in map(lambda x: x.questionId, user.favoriteQuestions.all()) else 'false'

    def get_type(self):
        return 'question'


class Answer(db.Model):
    __tablename__ = 'Answer'
    answerId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
    questionId = db.Column(db.BigInteger, db.ForeignKey('Question.questionId', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    answerTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    answerComments = db.relationship('AnswerComment', backref=db.backref('comments'), lazy='dynamic',
                                     cascade='all, delete-orphan')
    likeUsers = db.relationship('LikeAnswer', backref=db.backref('like_users'), lazy='dynamic',
                                cascade='all, delete-orphan')

    def get_user(self):
        return User.query.filter(User.id == self.userId).first().username

    def get_question(self):
        return Question.query.filter(Question.questionId == self.questionId).first()

    def is_user_like(self, user):
        return 'true' if self.answerId in map(lambda x: x.answerId, user.likeAnswers.all()) else 'false'

    def is_user_unlike(self, user):
        return 'true' if self.answerId in map(lambda x: x.answerId, user.unlikeAnswers.all()) else 'false'


class Article(db.Model):
    __tablename__ = 'Article'
    articleId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.Unicode(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publicTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    articleComments = db.relationship('ArticleComment', backref=db.backref('comments'), lazy='dynamic',
                                      cascade='all, delete-orphan')
    tags = db.relationship('ArticleTag', backref=db.backref('tags'), lazy='dynamic', cascade='all, delete-orphan')
    favoriteUsers = db.relationship('FavoriteArticle', backref=db.backref('favoriteUsers'), lazy='dynamic',
                                    cascade='all, delete-orphan')
    likeUsers = db.relationship('LikeArticle', backref=db.backref('like_users'), lazy='dynamic',
                                cascade='all, delete-orphan')
    unlikeUsers = db.relationship('UnlikeArticle', backref=db.backref('unlike_users'), lazy='dynamic',
                                  cascade='all, delete-orphan')

    @staticmethod
    def generate_fake(count=100):
        seed()
        user_count = User.query.count()
        for i in range(count):
            user = User.query.offset(randint(0, user_count - 1)).first()
            title = forgery_py.lorem_ipsum.sentence()
            if len(title) > 50:
                title = title[:20]
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

    def is_user_favorite(self, user):
        return 'true' if self.articleId in map(lambda x: x.articleId, user.favoriteArticles.all()) else 'false'

    def is_user_like(self, user):
        return 'true' if self.articleId in map(lambda x: x.articleId, user.likeArticles.all()) else 'false'

    def is_user_unlike(self, user):
        return 'true' if self.articleId in map(lambda x: x.articleId, user.unlikeArticles.all()) else 'false'

    def get_type(self):
        return 'article'


class Draft(db.Model):
    __tablename__ = 'Draft'
    draftId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.Unicode(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    saveTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def get_user(self):
        return User.query.filter(User.id == self.userId).first().name


class Tag(db.Model):
    __tablename__ = 'Tag'
    tagId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    parentId = db.Column(db.BigInteger, db.ForeignKey('Tag.tagId', ondelete='CASCADE'), nullable=True)
    name = db.Column(db.Unicode(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    popularity = db.Column(db.Integer, default=0, nullable=False)
    tagUsers = db.relationship('UserTag', backref=db.backref('users'), lazy='dynamic', cascade='all, delete-orphan')
    articles = db.relationship('ArticleTag', backref=db.backref('articles'), lazy='dynamic',
                               cascade='all, delete-orphan')
    problems = db.relationship('QuestionTag', backref=db.backref('problems'), lazy='dynamic',
                               cascade='all, delete-orphan')

    def __init__(self, parentId, name, description, popularity):
        self.parentId = parentId
        self.name = name
        self.description = description
        self.popularity = popularity

    def get_child_tags(self):
        return Tag.query.filter(Tag.parentId == self.tagId).all()

    # 将类转为字典，然后响应json
    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) \
                    for col in class_mapper(obj.__class__).mapped_table.c)


class ArticleComment(db.Model):
    __tablename__ = 'ArticleComment'
    commentId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
    parentId = db.Column(db.BigInteger, db.ForeignKey('ArticleComment.commentId', ondelete='CASCADE'), nullable=True)
    articleId = db.Column(db.BigInteger, db.ForeignKey('Article.articleId', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    commentTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # articleChildComments = db.relationship('ArticleComment', backref=db.backref('articleChildComments'))

    def get_user(self):
        return User.query.filter(User.id == self.userId).first().username

    def get_parent_comments(self):
        return ArticleComment.query.filter(ArticleComment.parentId is None).all()

    def get_child_comments(self):
        return ArticleComment.query.filter(ArticleComment.parentId == self.commentId).all()

    def get_parent_comment_user(self):
        return ArticleComment.query.filter(ArticleComment.commentId == self.parentId).first().get_user()


class AnswerComment(db.Model):
    __tablename__ = 'AnswerComment'
    commentId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    parentId = db.Column(db.BigInteger, db.ForeignKey('AnswerComment.commentId', ondelete='CASCADE'), nullable=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
    answerId = db.Column(db.BigInteger, db.ForeignKey('Answer.answerId', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    commentTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # answerChildComments = db.relationship('AnswerComment', backref=db.backref('answerChildComments'))

    def get_user(self):
        return User.query.filter(User.id == self.userId).first().username

    def get_parent_comment(self):
        return AnswerComment.query.filter(self.parentId == AnswerComment.commentId).first()

    def get_parent_comment_user(self):
        return AnswerComment.query.filter(self.parentId == AnswerComment.commentId).first().get_user()


class Notification(db.Model):
    __tablename__ = 'Notification'
    notificationId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.Unicode(200), nullable=False)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    isRead = db.Column(db.Boolean, default=False, nullable=False)
    notifyTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class LikeArticle(db.Model):
    __tablename__ = 'LikeArticle'
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
    articleId = db.Column(db.BigInteger, db.ForeignKey('Article.articleId', ondelete='CASCADE'), primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class LikeAnswer(db.Model):
    __tablename__ = 'LikeAnswer'
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
    answerId = db.Column(db.BigInteger, db.ForeignKey('Answer.answerId', ondelete='CASCADE'), primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class UnlikeArticle(db.Model):
    __tablename__ = 'UnlikeArticle'
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
    articleId = db.Column(db.BigInteger, db.ForeignKey('Article.articleId', ondelete='CASCADE'), primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class UnlikeAnswer(db.Model):
    __tablename__ = 'UnlikeAnswer'
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id', ondelete='CASCADE'), primary_key=True)
    answerId = db.Column(db.BigInteger, db.ForeignKey('Answer.answerId', ondelete='CASCADE'), primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
