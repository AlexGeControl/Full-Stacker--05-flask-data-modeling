import os

from application import create_app, db
from flask_migrate import Migrate

from application.models import Artist, Show, Venue
from init_db import init_all

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
Migrate(app, db)

# pop up db with init records:
# init_all(db=db, Artist=Artist, Show=Show, Venue=Venue)

@app.shell_context_processor
def make_shell_context():
    # make extra variables available in flask shell context:    
    return dict(db=db, Artist=Artist, Show=Show, Venue=Venue)