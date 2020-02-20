from flask import render_template

from application.main import main

@main.route('/')
@main.route('/index')
@main.route('/home')
def index():
    return render_template('index.html')