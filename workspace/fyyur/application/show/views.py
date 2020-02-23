from application import db
from application.models import Artist, Show, Venue

from flask import abort, render_template, request, flash, redirect, url_for

from . import bp
from .forms import ShowForm
from application.utils import convert_form_dict_to_dict

#  ----------------------------------------------------------------
#  routes
#  ----------------------------------------------------------------

#  CREATE
#  ----------------------------------------------------------------
@bp.route('/create')
def create_shows():
    """ render empty form
    """
    # load artists:
    artists = Artist.query.with_entities(
        Artist.id,
        Artist.name
    ).order_by(
        Artist.name
    ).all()
    # load venues:
    venues = Venue.query.with_entities(
        Venue.id,
        Venue.name
    ).order_by(
        Venue.name
    ).all()    

    # create form:
    form = ShowForm()
    form.artist_id.choices = [
        (artist.id, artist.name) for artist in artists
    ]
    form.venue_id.choices = [
        (venue.id, venue.name) for venue in venues
    ]

    return render_template('forms/new_show.html', form=form)

@bp.route('/create', methods=['POST'])
def create_show_submission():
    """ create new venue using POSTed form
    """
    # parse POSTed form:
    show_created = convert_form_dict_to_dict(request.form)

    try:
        show = Show(**show_created)
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Your show could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')

#  READ
#  ----------------------------------------------------------------
@bp.route('/')
def shows():
    ''' list shows
    '''
    # artists:
    artists_subq = Artist.query.with_entities(
        Artist.id,
        Artist.name,
        Artist.image_link
    ).subquery()
    # venues:
    venues_subq = Venue.query.with_entities(
        Venue.id,
        Venue.name,
        Venue.image_link
    ).subquery()
    # shows:
    shows_subq = Show.query.with_entities(
        Show.start_time,
        Show.artist_id,
        Show.venue_id
    ).subquery()
    
    # join
    data = db.session.query(
        venues_subq.c.id,
        venues_subq.c.name,
        artists_subq.c.id,
        artists_subq.c.name,
        artists_subq.c.image_link,
        shows_subq.c.start_time
    ).join(
        artists_subq, shows_subq.c.artist_id == artists_subq.c.id
    ).join(
        venues_subq, shows_subq.c.venue_id == venues_subq.c.id 
    ).all()

    # format:
    shows = [
        {
            "venue_id": venue_id,
            "venue_name": venue_name,
            "artist_id": artist_id,
            "artist_name": artist_name,
            "artist_image_link": artist_image_link,
            "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        } for (venue_id, venue_name, artist_id, artist_name, artist_image_link, start_time) in data
    ]

    return render_template('pages/shows.html', shows=shows)
