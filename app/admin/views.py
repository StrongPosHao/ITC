from flask import render_template
from . import admin


@admin.route('/')
def test():
    return render_template('admin/index.html')
