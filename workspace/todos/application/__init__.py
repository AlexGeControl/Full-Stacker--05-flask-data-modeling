from flask import Flask

from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
moment = Moment()

def create_app(config_name):
    app = Flask(__name__)
    # load configs:
    app.config.from_object(config[config_name])    
    config[config_name].init_app(app)    
    
    # activate extensions:
    db.init_app(app)
    moment.init_app(app)

    # attach routes and custom error pages here    
    from .main import bp as blueprint_main
    app.register_blueprint(blueprint_main)

    from .todo import bp as blueprint_todo
    app.register_blueprint(blueprint_todo, url_prefix='/todos')

    return app