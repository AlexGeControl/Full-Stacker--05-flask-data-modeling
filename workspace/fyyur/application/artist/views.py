from application import db
from application.models import Artist

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
    # fetch data:
    data = Artist.query.with_entities(
        Artist.id,
        Artist.name
    ).all()

    artists=[
        {
            "id": id,
            "name": name,
        } for (id, name) in data
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

    data = Artist.query.with_entities(
        Artist.id,
        Artist.name
    ).filter(
        Artist.name.contains(keyword)
    ).all()

    results={
        "count": len(data),
        "data": [
            {
                "id": id,
                "name": name,
                "num_upcoming_shows": 0,
            } for (id, name) in data
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
    '''
    data1={
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "past_shows": [
            {
                "venue_id": 1,
                "venue_name": "The Musical Hop",
                "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
                "start_time": "2019-05-21T21:30:00.000Z"
            }
        ],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data2={
        "id": 5,
        "name": "Matt Quevedo",
        "genres": ["Jazz"],
        "city": "New York",
        "state": "NY",
        "phone": "300-400-5000",
        "facebook_link": "https://www.facebook.com/mattquevedo923251523",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "past_shows": [
            {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2019-06-15T23:00:00.000Z"
            }
        ],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data3={
        "id": 6,
        "name": "The Wild Sax Band",
        "genres": ["Jazz", "Classical"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "432-325-5432",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "past_shows": [],
        "upcoming_shows": [
            {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-01T20:00:00.000Z"
            }, {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-08T20:00:00.000Z"
            }, {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-15T20:00:00.000Z"
            }
        ],
        "past_shows_count": 0,
        "upcoming_shows_count": 3,
    }
    data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

    return render_template('pages/show_artist.html', artist=data)
    '''
    # shows the artist page with the given artist_id
    data = Artist.query.get_or_404(artist_id, description='There is no artist with id={}'.format(artist_id)).to_json()

    # TODO: past & upcoming shows generation
    data["past_shows"] = []
    data["upcoming_shows"] = []
    data["past_shows_count"] = len(data["past_shows"])
    data["upcoming_shows_count"] = len(data["upcoming_shows"])

    return render_template('pages/show_artist.html', artist=data)    

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