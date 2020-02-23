from application import db
from application.models import Artist, Show, Venue
from sqlalchemy import func
from datetime import datetime

from flask import abort, render_template, request, flash, redirect, url_for

from . import bp
from .forms import ArtistForm
from application.utils import convert_form_dict_to_dict

#  ----------------------------------------------------------------
#  routes
#  ----------------------------------------------------------------

#  CREATE
#  ----------------------------------------------------------------
@bp.route('/create', methods=['GET'])
def create_artist_form():
    """ render empty form
    """
    form = ArtistForm()

    return render_template('forms/new_artist.html', form=form)

@bp.route('/create', methods=['POST'])
def create_artist_submission():
    """ create new artist using POSTed form
    """
    # parse POSTed form:
    artist_created = convert_form_dict_to_dict(request.form)
    # parse artist name:
    artist_name = artist_created["name"]

    try:
        artist = Artist(**artist_created)
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + artist_name + ' was successfully listed!')
    except:
        db.session.rollback()
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist ' + artist_name + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')

#  READ
#  ----------------------------------------------------------------
@bp.route('/', methods=['GET'])
def artists():
    """ list all artists
    """
    # data:
    shows_subq = Show.query.with_entities(
        Show.artist_id,
        func.count(Show.artist_id).label('num_upcoming_shows')
    ).filter(
        Show.start_time > datetime.utcnow()
    ).group_by(
        Show.artist_id
    ).subquery()

    data = db.session.query(
        Artist.id,
        Artist.name,
        shows_subq.c.num_upcoming_shows
    ).join(
        shows_subq, Artist.id == shows_subq.c.artist_id
    ).all()

    artists=[
        {
            "id": id,
            "name": name,
            "num_upcoming_shows": num_upcoming_shows
        } for (id, name, num_upcoming_shows) in data
    ]
    
    return render_template('pages/artists.html', artists=artists)

@bp.route('/search', methods=['GET'])
def search_artists_form():
    """ search on artists names with partial string search. case-insensitive.
    """
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    return render_template(
        'pages/search_artists.html'
    )

@bp.route('/search', methods=['POST'])
def search_artists_submission():
    """ search on artists names with partial string search. case-insensitive.
    """
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    keyword = request.form.get('keyword', '')

    # data:
    shows_subq = Show.query.with_entities(
        Show.artist_id,
        func.count(Show.artist_id).label('num_upcoming_shows')
    ).filter(
        Show.start_time > datetime.utcnow()
    ).group_by(
        Show.artist_id
    ).subquery()

    artists_subq = Artist.query.with_entities(
        Artist.id,
        Artist.name
    ).filter(
        Artist.name.contains(keyword)
    ).subquery()

    data = db.session.query(
        artists_subq.c.id,
        artists_subq.c.name,
        shows_subq.c.num_upcoming_shows
    ).join(
        shows_subq, artists_subq.c.id == shows_subq.c.artist_id
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
        'pages/search_artists.html', 
        results=results, keyword=keyword
    )

@bp.route('/<int:artist_id>')
def show_artist(artist_id):
    """ show given artist
    """
    # shows the artist page with the given artist_id
    artist = Artist.query.get_or_404(artist_id, description='There is no artist with id={}'.format(artist_id)).to_json()

    # fetch contracted artists: 
    shows_subq = Show.query.with_entities(
        Show.start_time,
        Show.artist_id,
        Show.venue_id
    ).filter_by(
        artist_id = artist['id']
    ).subquery()

    venues_subq = Venue.query.with_entities(
        Venue.id,
        Venue.name,
        Venue.image_link
    ).subquery()

    contracted_shows = db.session.query(
        shows_subq.c.venue_id,
        venues_subq.c.name,
        venues_subq.c.image_link,
        shows_subq.c.start_time
    ).join(
        venues_subq, shows_subq.c.venue_id == venues_subq.c.id
    ).all()

    # format:
    artist["past_shows"] = []
    artist["upcoming_shows"] = []

    current_time = datetime.utcnow()
    for (venue_id, venue_name, venue_image_link, start_time) in contracted_shows:
        show = {
            "venue_id": venue_id, 
            "venue_name": venue_name, 
            "venue_image_link": venue_image_link, 
            "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        if start_time < current_time:
            artist["past_shows"].append(show)
        else:
            artist["upcoming_shows"].append(show)

    artist["past_shows_count"] = len(artist["past_shows"])
    artist["upcoming_shows_count"] = len(artist["upcoming_shows"])

    return render_template('pages/show_artist.html', artist=artist)    

#  UPDATE
#  ----------------------------------------------------------------
@bp.route('/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """ render form pre-filled with given artist
    """
    artist = Artist.query.get_or_404(artist_id, description='There is no artist with id={}'.format(artist_id))
    form = ArtistForm(obj = artist)

    return render_template('forms/edit_artist.html', form=form, artist=artist)

@bp.route('/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    """ edit artist using POSTed form
    """
    # parse POSTed form:
    artist_updated = convert_form_dict_to_dict(request.form)
    # parse artist name:
    artist_name = artist_updated["name"]

    try:
        # read:
        artist = Artist.query.get_or_404(artist_id, description='There is no artist with id={}'.format(artist_id))
        # update:
        artist.from_json(artist_updated)
        db.session.add(artist)
        # write
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + artist_name + ' was successfully updated!')
    except:
        db.session.rollback()
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist ' + artist_name + ' could not be updated.')
    finally:
        db.session.close()

    return redirect(url_for('.show_artist', artist_id=artist_id))

#  DELETE
#  ----------------------------------------------------------------
@bp.route('/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    """ delete artist
    """
    error = True

    try:
        # find:
        artist = Artist.query.get_or_404(artist_id, description='There is no artist with id={}'.format(artist_id))
        artist_name = artist.name
        db.session.delete(artist)
        # write
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + artist_name + ' was successfully deleted!')
        error = False
    except:
        db.session.rollback()
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist could not be deleted.')
        error = True
    finally:
        db.session.close()

    if error:
        abort(400)

    return render_template('pages/home.html')