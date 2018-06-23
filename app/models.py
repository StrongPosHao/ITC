from app.exts import db
from datetime import datetime


class Follow(db.Model):
    __tablename__ = 'Follow'
    followerId = db.Column(db.BigInteger, db.ForeignKey('User.userId'), primary_key=True)
    followedId = db.Column(db.BigInteger, db.ForeignKey('User.userId'), primary_key=True)
    followTime = db.Column(db.DateTime, default=datetime.now())


class UserTag(db.Model):
    __tablename__ = 'UserTag'
    userId = db.Column(db.BigInteger, db.ForeignKey('User.userId'), primary_key=True, nullable=False)
    tagId = db.Column(db.BigInteger, db.ForeignKey('Tag.tagId'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class ArticleTag(db.Model):
    __tablename__ = 'ArticleTag'
    articleId = db.Column(db.BigInteger, db.ForeignKey('Article.articleId'), primary_key=True, nullable=False)
    tagId = db.Column(db.BigInteger, db.ForeignKey('Tag.tagId'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class QuestionTag(db.Model):
    __tablename__ = 'QuestionTag'
    questionId = db.Column(db.BigInteger, db.ForeignKey('Question.questionId'), primary_key=True, nullable=False)
    tagId = db.Column(db.BigInteger, db.ForeignKey('Tag.tagId'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class FavoriteArticle(db.Model):
    __tablename__ = 'FavoriteArticle'
    articleId = db.Column(db.BigInteger, db.ForeignKey('Article.articleId'), primary_key=True, nullable=False)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.userId'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class FavoriteQuestion(db.Model):
    __tablename__ = 'FavoriteQuestion'
    questionId = db.Column(db.BigInteger, db.ForeignKey('Question.questionId'), primary_key=True, nullable=False)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.userId'), primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class User(db.Model):
    __tablename__ = 'User'
    userId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userName = db.Column(db.Unicode(20), nullable=False)
    email = db.Column(db.Unicode(64), nullable=False)
    phone = db.Column(db.CHAR(11), nullable=False)
    password = db.Column(db.Unicode(100), nullable=False)
    headImage = db.Column(db.Unicode(256), nullable=False)
    permission = db.Column(db.CHAR(1), nullable=False)
    introduction = db.Column(db.Text, default='这家伙很懒，什么也没有写~', nullable=False)
    tags = db.relationship('UserTag', foreign_keys=[UserTag.tagId],
                           backref=db.backref('tags'),
                           lazy='dynamic',
                           cascade='all, delete-orphan')
    articles = db.relationship('Article', backref=db.backref('articles'))
    questions = db.relationship('Question', backref=db.backref('questions'))
    drafts = db.relationship('Draft', backref=db.backref('drafts'))
    answers = db.relationship('Answer', backref=db.backref('answers'))
    followed = db.relationship('Follow', foreign_keys=[Follow.followerId],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.followedId],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    favoriteArticles = db.relationship('FavoriteArticle', foreign_keys=[FavoriteArticle.articleId],
                                       backref=db.backref('articles', lazy='joined'),
                                       lazy='dynamic',
                                       cascade='all, delete-orphan')
    favoriteQuestions = db.relationship('FavoriteQuestion', foreign_keys=[FavoriteQuestion.questionId],
                                        backref=db.backref('questions', lazy='joined'),
                                        lazy='dynamic',
                                        cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref=db.backref('notifications'))


class Admin(db.Model):
    __tablename__ = 'Admin'
    adminId = db.Column(db.BigInteger, primary_key=True, nullable=False)
    adminName = db.Column(db.Unicode(20), nullable=False)
    email = db.Column(db.Unicode(64), nullable=False)
    phone = db.Column(db.CHAR(11), nullable=False)
    password = db.Column(db.Unicode(100), nullable=False)
    headImage = db.Column(db.Unicode(256), nullable=False)
    permission = db.Column(db.CHAR(1), nullable=False)


class Question(db.Model):
    __tablename__ = 'Question'
    questionId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.Unicode(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publicTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    answers = db.relationship('Answer', backref=db.backref('answers'))
    tags = db.relationship('QuestionTag', foreign_keys=[QuestionTag.tagId], backref=db.backref('tags', lazy='joined'),
                           lazy='dynamic',
                           cascade='all, delete-orphan')
    favoriteUsers = db.relationship('FavoriteQuestion', foreign_keys=[FavoriteQuestion.userId],
                                    lazy='dynamic',
                                    cascade='all, delete-orphan')


class Answer(db.Model):
    __tablename__ = 'Answer'
    answerId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.userId'), nullable=False)
    questionId = db.Column(db.BigInteger, db.ForeignKey('Question.questionId'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    answerTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class Article(db.Model):
    __tablename__ = 'Article'
    articleId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.userId'), nullable=False)
    title = db.Column(db.Unicode(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publicTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    tags = db.relationship('ArticleTag', foreign_keys=[ArticleTag.tagId], backref=db.backref('tags', lazy='joined'),
                           lazy='dynamic',
                           cascade='all, delete-orphan')
    favoriteUsers = db.relationship('FavoriteArticle', foreign_keys=[FavoriteArticle.userId],
                                    backref=db.backref('favoriteUsers', lazy='joined'),
                                    lazy='dynamic',
                                    cascade='all, delete-orphan')


class Draft(db.Model):
    __tablename__ = 'Draft'
    draftId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.userId'), nullable=False)
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
    tagUsers = db.relationship('UserTag', foreign_keys=[UserTag.userId],
                               backref=db.backref('users', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    articles = db.relationship('ArticleTag', foreign_keys=[ArticleTag.articleId],
                               backref=db.backref('articles', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    problems = db.relationship('ProblemTag', foreign_keys=[QuestionTag.questionId],
                               backref=db.backref('problems', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')


class ArticleComment(db.Model):
    __tablename__ = 'ArticleComment'
    commentId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    parentId = db.Column(db.BigInteger, db.ForeignKey('ArticleComment.commentId'), nullable=True)
    articleId = db.Column(db.BigInteger, db.ForeignKey('Article.articleId'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    commentTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    childComments = db.relationship('ArticleComment', backref=db.backref('childComments'))


class AnswerComment(db.Model):
    __tablename__ = 'AnswerComment'
    commentId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    parentId = db.Column(db.BigInteger, db.ForeignKey('AnswerComment.commentId'), nullable=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.userId'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    commentTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    childComments = db.relationship('AnswerComment', backref=db.backref('childComments'))


class Notification(db.Model):
    __tablename__ = 'Notification'
    notificationId = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.userId'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    isRead = db.Column(db.Boolean, default=False, nullable=False)
    notifyTime = db.Column(db.DateTime, default=datetime.now(), nullable=False)


