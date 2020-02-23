from datetime import datetime
from flask_wtf import Form
from wtforms import SelectField, DateTimeField
from wtforms.validators import DataRequired


class ShowForm(Form):
    # start time:
    start_time = DateTimeField(
        'start_time',
        validators=[
            DataRequired()
        ],
        default= datetime.today()
    )
    
    # artist:
    artist_id = SelectField(
        'artist_id', 
        choices=[], 
        coerce=int
    )
    # venue:
    venue_id = SelectField(
        'venue_id', 
        choices=[], 
        coerce=int
    )
