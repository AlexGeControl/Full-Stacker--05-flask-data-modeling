import os

class Config:
    # security:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # database:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # mail service:
    """
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    """

    @staticmethod
    def init_app(app):
        """ integrate with app factory
        """
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # database:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'todos-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    # database:
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    # database:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'todos.sqlite')

# root dir of app:
basedir = os.path.abspath(os.path.dirname(__file__))

# configs:
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}