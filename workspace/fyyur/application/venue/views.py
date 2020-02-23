from application import db
from application.models import Artist, Show, Venue
from sqlalchemy import func
from datetime import datetime

from flask import abort, render_template, request, flash, redirect, url_for

from . import bp
from .forms import VenueForm
from application.utils import convert_form_dict_to_dict
from itertools import groupby

#  ----------------------------------------------------------------
#  routes
#  ----------------------------------------------------------------

#  CREATE
#  ----------------------------------------------------------------
@bp.route('/create', methods=['GET'])
def create_venue_form():
    """ render empty form
    """
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@bp.route('/create', methods=['POST'])
def create_venue_submission():
    """ create new venue using POSTed form
    """
    # parse POSTed form:
    venue_created = convert_form_dict_to_dict(request.form)
    # parse venue name:
    venue_name = venue_created["name"]

    try:
        venue = Venue(**venue_created)
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + venue_name + ' was successfully listed!')
    except:
        db.session.rollback()
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' + venue_name + ' could not be listed.')
    finally:
        db.session.close()
    
    return render_template('pages/home.html')

#  READ
#  ----------------------------------------------------------------
@bp.route('/', methods=['GET'])
def venues():
    """ list all venues
    """
    # data:
    shows_subq = Show.query.with_entities(
        Show.venue_id,
        func.count(Show.venue_id).label('num_upcoming_shows')
    ).filter(
        Show.start_time > datetime.utcnow()
    ).group_by(
        Show.venue_id
    ).subquery()

    data = db.session.query(
        Venue.city,
        Venue.state,
        Venue.id,
        Venue.name,
        shows_subq.c.num_upcoming_shows
    ).join(
        shows_subq, Venue.id == shows_subq.c.venue_id
    ).all()

    # format:
    areas = [
        {
            "city": city,
            "state": state,
            "venues": [
                {
                    "id": id,
                    "name": name,
                    "num_upcoming_shows": num_upcoming_shows,
                } for (_, _, id, name, num_upcoming_shows) in venues               
            ]
        } for (city, state), venues in groupby(data, lambda x: (x[0], x[1]))
    ]

    return render_template(
        "pages/venues.html", 
        areas=areas
    )

@bp.route('/search', methods=['GET'])
def search_venues_form():
    """ search on venue names with partial string search. case-insensitive.
    """
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    return render_template(
        'pages/search_venues.html'
    )

@bp.route('/search', methods=['POST'])
def search_venues_submission():
    """ search on venue names with partial string search. case-insensitive.
    """
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    keyword = request.form.get('keyword', '')
    
    # data:
    shows_subq = Show.query.with_entities(
        Show.venue_id,
        func.count(Show.venue_id).label('num_upcoming_shows')
    ).filter(
        Show.start_time > datetime.utcnow()
    ).group_by(
        Show.venue_id
    ).subquery()

    venues_subq = Venue.query.with_entities(
        Venue.id,
        Venue.name
    ).filter(
        Venue.name.contains(keyword)
    ).subquery()

    data = db.session.query(
        venues_subq.c.id,
        venues_subq.c.name,
        shows_subq.c.num_upcoming_shows
    ).join(
        shows_subq, venues_subq.c.id == shows_subq.c.venue_id
    ).all()

    results={
        "count": len(data),
        "data": [
            {
                "id": id,
                "name": name,
                "num_upcoming_shows": num_upcoming_shows,
            } for (id, name, num_upcoming_shows) in data
        ]
    }

    return render_template(
        'pages/search_venues.html', 
        results=results, keyword=keyword
    )

@bp.route('/<int:venue_id>')
def show_venue(venue_id):
    """ show given venue
    """
    # get venue:
    venue = Venue.query.get_or_404(venue_id, description='There is no venue with id={}'.format(venue_id)).to_json()

    # fetch contracted artists: 
    shows_subq = Show.query.with_entities(
        Show.start_time,
        Show.venue_id,
        Show.artist_id
    ).filter_by(
        venue_id = venue['id']
    ).subquery()

    artists_subq = Artist.query.with_entities(
        Artist.id,
        Artist.name,
        Artist.image_link
    ).subquery()

    contracted_shows = db.session.query(
        shows_subq.c.artist_id,
        artists_subq.c.name,
        artists_subq.c.image_link,
        shows_subq.c.start_time
    ).join(
        artists_subq, shows_subq.c.artist_id == artists_subq.c.id
    ).all()

    # format:
    venue["past_shows"] = []
    venue["upcoming_shows"] = []

    current_time = datetime.utcnow()
    for (artist_id, artist_name, artist_image_link, start_time) in contracted_shows:
        show = {
            "artist_id": artist_id, 
            "artist_name": artist_name, 
            "artist_image_link": artist_image_link, 
            "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        if start_time < current_time:
            venue["past_shows"].append(show)
        else:
            venue["upcoming_shows"].append(show)

    venue["past_shows_count"] = len(venue["past_shows"])
    venue["upcoming_shows_count"] = len(venue["upcoming_shows"])

    return render_template('pages/show_venue.html', venue=venue)

#  UPDATE
#  ----------------------------------------------------------------
@bp.route('/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    """ render form pre-filled with venue
    """
    venue = Venue.query.get_or_404(venue_id, description='There is no venue with id={}'.format(venue_id))
    form = VenueForm(obj=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)

@bp.route('/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    """ edit venue using POSTed form
    """
    # parse POSTed form:
    venue_updated = convert_form_dict_to_dict(request.form)
    # parse venue name:
    venue_name = venue_updated["name"]

    try:
        # read:
        venue = Venue.query.get_or_404(venue_id, description='There is no venue with id={}'.format(venue_id))
        # update:
        venue.from_json(venue_updated)
        db.session.add(venue)
        # write
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + venue_name + ' was successfully updated!')
    except:
        db.session.rollback()
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' + venue_name + ' could not be updated.')
    finally:
        db.session.close()

    return redirect(url_for('venue.show_venue', venue_id=venue_id))

#  DELETE
#  ----------------------------------------------------------------
@bp.route('/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    """ delete venue
    """
    error = True

    try:
        # find:
        venue = Venue.query.get_or_404(venue_id, description='There is no venue with id={}'.format(venue_id))
        venue_name = venue.name
        db.session.delete(venue)
        # write
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + venue_name + ' was successfully deleted!')
        error = False
    except:
        db.session.rollback()
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue could not be deleted.')
        error = True
    finally:
        db.session.close()

    if error:
        abort(400)

    return render_template('pages/home.html')