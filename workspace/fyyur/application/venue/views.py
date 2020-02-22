from application import db
from application.models import Venue

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
@bp.route('/', methods=['GET', 'DELETE'])
def venues():
    # fetch data:
    data = Venue.query.with_entities(
        Venue.city,
        Venue.state,
        Venue.id,
        Venue.name
    ).group_by(
        Venue.id,
        Venue.name
    ).all()

    # format as areas:
    areas = [
        {
            "city": city,
            "state": state,
            "venues": [
                {
                    "id": id,
                    "name": name,
                    # TODO: upcoming show count generation
                    "num_upcoming_shows": 0,
                } for (_, _, id, name) in venues               
            ]
        } for (city, state), venues in groupby(data, lambda x: (x[0], x[1]))
    ]


    return render_template(
        "pages/venues.html", 
        areas=areas
    )

@bp.route('/search', methods=['POST'])
def search_venues():
    """ search on venue names with partial string search. case-insensitive.
    """
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')

    data = Venue.query.with_entities(
        Venue.id,
        Venue.name
    ).filter(
        Venue.name.ilike(search_term)
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
        'pages/search_venues.html', 
        results=results, search_term=search_term
    )

@bp.route('/<int:venue_id>')
def show_venue(venue_id):
    """ show given venue
    """
    '''
    data1={
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "past_shows": [
            {
                "artist_id": 4,
                "artist_name": "Guns N Petals",
                "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
                "start_time": "2019-05-21T21:30:00.000Z"
            }
        ],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data2={
        "id": 2,
        "name": "The Dueling Pianos Bar",
        "genres": ["Classical", "R&B", "Hip-Hop"],
        "address": "335 Delancey Street",
        "city": "New York",
        "state": "NY",
        "phone": "914-003-1132",
        "website": "https://www.theduelingpianos.com",
        "facebook_link": "https://www.facebook.com/theduelingpianos",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }
    data3={
        "id": 3,
        "name": "Park Square Live Music & Coffee",
        "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
        "address": "34 Whiskey Moore Ave",
        "city": "San Francisco",
        "state": "CA",
        "phone": "415-000-1234",
        "website": "https://www.parksquarelivemusicandcoffee.com",
        "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        "seeking_talent": False,
        "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "past_shows": [
            {
                "artist_id": 5,
                "artist_name": "Matt Quevedo",
                "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
                "start_time": "2019-06-15T23:00:00.000Z"
            }
        ],
        "upcoming_shows": [
            {
                "artist_id": 6,
                "artist_name": "The Wild Sax Band",
                "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                "start_time": "2035-04-01T20:00:00.000Z"
            }, {
                "artist_id": 6,
                "artist_name": "The Wild Sax Band",
                "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                "start_time": "2035-04-08T20:00:00.000Z"
            }, {
                "artist_id": 6,
                "artist_name": "The Wild Sax Band",
                "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                "start_time": "2035-04-15T20:00:00.000Z"
            }
        ],
        "past_shows_count": 1,
        "upcoming_shows_count": 1,
    }
    data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

    return render_template('pages/show_venue.html', venue=data)
    '''
    # shows the venue page with the given venue_id
    data = Venue.query.get_or_404(venue_id, description='There is no venue with id={}'.format(venue_id)).to_json()

    # TODO: past & upcoming shows generation
    data["past_shows"] = []
    data["upcoming_shows"] = []
    data["past_shows_count"] = len(data["past_shows"])
    data["upcoming_shows_count"] = len(data["upcoming_shows"])

    return render_template('pages/show_venue.html', venue=data)

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
    print(venue_updated)

    try:
        # read:
        venue = Venue.query.get_or_404(venue_id, description='There is no venue with id={}'.format(venue_id))
        # update:
        print(repr(venue))
        venue.from_json(venue_updated)
        print(repr(venue))
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

    return redirect(url_for('.venues'))