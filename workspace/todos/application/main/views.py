from application import db
from application.models import Todo

from flask import render_template

from . import bp

@bp.route('/')
@bp.route('/index')
@bp.route('/home')
def index():
    """ home page
    """
    return render_template('index.html', data=Todo.query.all())