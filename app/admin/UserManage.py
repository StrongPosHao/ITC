from flask import render_template
from . import admin


@admin.route('/user1')
def test1():
    return render_template('admin/UserManage.html')
