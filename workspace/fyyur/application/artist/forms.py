from datetime import datetime
from flask_wtf import Form
from wtforms import BooleanField, StringField, TextAreaField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, Optional, URL, Regexp


class ArtistForm(Form):
    # personal info:
    name = StringField(
        'name', 
        validators = [
            DataRequired()
        ]
    )
    image_link = StringField(
        'image_link', 
        validators = [
            Optional(), URL()
        ]
    )
    # address:
    city = StringField(
        'city', 
        validators = [
            DataRequired()
        ]
    )
    state = SelectField(
        'state', 
        validators = [
            DataRequired()
        ],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    # contact:
    phone = StringField(
        'phone',
        validators=[
            DataRequired(), 
            Regexp('^\d{3}-\d{3}-\d{4}$', message="Please fill out a valid phone number.")
        ]
    )
    website = StringField(
        'website', 
        validators=[
            Optional(), 
            URL()
        ]
    )
    facebook_link = StringField(
        'facebook_link', 
        validators = [
            Optional(), 
            URL()
        ]
    )
    # genres:
    genres = SelectMultipleField(
        'genres', 
        validators = [
            DataRequired()
        ],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    # venue seeking:
    seeking_venue = BooleanField(
        'seeking_venue',
        validators = [
            Optional()
        ]
    )
    seeking_description = TextAreaField(
        'seeking_description',
        validators = [
            Optional()
        ]
    )
