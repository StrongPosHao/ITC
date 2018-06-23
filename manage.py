from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.exts import db
from app.models import *
from app import create_app

app = create_app()
manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Follow=Follow, UserTag=UserTag, ArticleTag=ArticleTag, QuestionTag=QuestionTag,
                FavoriteArticle=FavoriteArticle, FavoriteQuestion=FavoriteQuestion, User=User, Admin=Admin,
                Question=Question, Answer=Answer, Article=Article, Draft=Draft, Tag=Tag, ArticleComment=ArticleComment,
                AnswerComment=AnswerComment, Notification=Notification)


manager.add_command("shell", Shell(make_context=make_shell_context))

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
