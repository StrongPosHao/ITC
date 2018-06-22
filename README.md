# ITC
Internet Technology Community 

This is our Python final task.

Team member

* WuKangjun
* ZhangHao
* ChenJin
* XuYanan
* DaXinyong

Notice:
* 项目运行入口为manage.py
    * PyCharm直接右键run
    * 命令行下 $ python manage.py runserver
* 项目结构<br>
![image](https://raw.githubusercontent.com/StrongPosHao/MarkdownPhotos/master/ProjectStructure.png)
* 缺失的config.py在群文件中下载

项目结构说明
* 最外层的requirements.txt是该项目的Python依赖库, 可使用 $ python install -r requirements.txt进行所有依赖库的安装或直接使用PyCharm进行安装
* migrations文件夹存放数据库相关迁移文件，**勿动**
* app
    * \_\_init__.py存放app的构造工厂函数，其包含对app的配置加载以及Blueprint的注册
    * email.py用于处理邮件相关的功能模块
    * exts.py用于解除包之间的循环依赖
    * models.py用于存放数据库模型
    * static用来存放相关静态资源, 相应的用途见各文件夹的README
    * templates用来存放相关模板，子目录名称与相应的Web模块对应
    * admin, article, auth, main为相应的Web模块，均使用Blueprint实现, url前缀与模块名对应
        * admin对应管理员模块
        * article对应文章模块
        * auth对应用户认证模块(登录、注册等)
        * main对应主页模块
    
    
* 对于Web模块目录，以main举例
    * \_\_init__.py用于对该模块的蓝图进行初始化
    * views.py用于存放视图函数
    * errors.py用于处理错误页面(404, 500等, 如果有需要的话...)
