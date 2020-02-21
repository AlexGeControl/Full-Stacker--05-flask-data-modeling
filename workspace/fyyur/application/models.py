# TODO: connect to a local postgresql database
from application import db

# pgsql array
from sqlalchemy.dialects.postgresql import ARRAY

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
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

    phone = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)

    genres = db.Column(ARRAY(db.String), nullable=False)

    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    
    def to_json(self):
        """ map venue object to python dict
        """
        data = {
            "name": self.name,

            "city": self.city,
            "state": self.state,
            "address": self.address,

            "image_link": self.image_link,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,

            "genres": self.genres,

            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description
        }

        return data

class Artist(db.Model):
    """ table artists
    """
    # follow the best practice
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    genres = db.Column(ARRAY(db.String), nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    """ table shows
    """
    # follow the best practice
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)