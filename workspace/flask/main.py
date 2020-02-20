import os

from application import create_app, db

from application.models import Role, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
        
    return dict(db=db, User=User, Role=Role)