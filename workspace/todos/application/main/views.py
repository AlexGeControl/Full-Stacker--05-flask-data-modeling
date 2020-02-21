from application import db
from application.models import TodoList, Todo

from flask import render_template

from . import bp

@bp.route('/')
@bp.route('/index')
@bp.route('/home')
def index():
    """ home page
    """
    lists = TodoList.query.all()
    todos = TodoList.query.first().todos

    return render_template('index.html', lists=lists, todos=todos)