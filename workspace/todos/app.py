import os

from application import create_app, db
from flask_migrate import Migrate

from application.models import Todo

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    # make extra variables available in flask shell context:    
    return dict(db=db, Todo=Todo)