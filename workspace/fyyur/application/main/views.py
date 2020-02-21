from flask import render_template

from . import main

@main.route('/')
@main.route('/index')
@main.route('/home')
def index():
    """ home page
    """
    return render_template('pages/home.html')