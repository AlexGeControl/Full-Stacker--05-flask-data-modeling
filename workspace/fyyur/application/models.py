from application import db

# pgsql array
from sqlalchemy.dialects.postgresql import ARRAY

from datetime import datetime

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Artist(db.Model):
    """ table artists
    """
    # follow the best practice
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String(500), nullable=True)

    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)

    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)

    genres = db.Column(ARRAY(db.String), nullable=False)

    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)

    # relationship:
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return f'<Artist id="{self.id}" name="{self.name}" city="{self.city}" state="{self.state}">'

    def to_json(self):
        """ map artist object to python dict
        """
        data = {
            "id": self.id,

            "name": self.name,
            "image_link": self.image_link,

            "city": self.city,
            "state": self.state,

            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,

            "genres": self.genres,

            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description
        }

        return data

    def from_json(self, json):
        """ update artist object using python dict input
        """
        self.name = json.get('name', '')
        self.image_link = json.get('image_link', '')
        
        self.city = json.get('city', '')
        self.state = json.get('state', '')

        self.phone = json.get('phone', '')
        self.website = json.get('website', '')
        self.facebook_link = json.get('facebook_link', '')

        self.genres = json.get('genres', [])

        self.seeking_venue = (json.get('seeking_venue', 'n') == 'y')
        self.seeking_description = json.get('seeking_description', '')


class Venue(db.Model):
    """ table venues
    """
    # follow the best practice
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String(500), nullable=True)

    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)

    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)

    genres = db.Column(ARRAY(db.String), nullable=False)

    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)

    # relationship:
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f'<Venue id="{self.id}" name="{self.name}" city="{self.city}" state="{self.state}">'

    def to_json(self):
        """ map venue object to python dict
        """
        data = {
            "id": self.id,

            "name": self.name,
            "image_link": self.image_link,

            "city": self.city,
            "state": self.state,
            "address": self.address,

            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,

            "genres": self.genres,

            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description
        }

        return data

    def from_json(self, json):
        """ update venue object using python dict input
        """
        self.name = json.get('name', '')
        self.image_link = json.get('image_link', '')
        
        self.city = json.get('city', '')
        self.state = json.get('state', '')
        self.address = json.get('address', '')

        self.phone = json.get('phone', '')
        self.website = json.get('website', '')
        self.facebook_link = json.get('facebook_link', '')

        self.genres = json.get('genres', [])

        self.seeking_talent = (json.get('seeking_talent', 'n') == 'y')
        self.seeking_description = json.get('seeking_description', '')


class Show(db.Model):
    """ table shows
    """
    # follow the best practice
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)

    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # relationship
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=True)

    def __repr__(self):
        return f'<Show id="{self.id}" artist_id="{self.artist_id}" venue_id="{self.venue_id}">'

    def to_json(self):
        """ map show object to python dict
        """
        data = {
            "id": self.id,
            "start_time": self.start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "artist_id": self.artist_id,
            "venue_id": self.venue_id
        }

        return data

    def from_json(self, json):
        """ update show object using python dict input
        """
        self.start_time = datetime.utcnow if (not 'start_time' in json) else datetime.strptime(json['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        
        self.artist_id = int(json['artist_id'])
        self.venue_id = int(json['venue_id'])