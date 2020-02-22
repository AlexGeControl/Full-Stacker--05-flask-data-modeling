import json

def init_venues(db, Venue):
    """ load init venues from json
    """
    with open('data/venues.json') as venues_json_file:
        venues = json.load(venues_json_file)
 
    success = False
    try:
        for venue in venues:
            db.session.add(Venue(**venue))
        db.session.commit()
        success = True
    except:
        db.session.rollback()
        success=False
    finally:
        db.session.close()

    return success

def init_artists(db, Artist):
    """ load init artists from json
    """
    with open('data/artists.json') as artists_json_file:
        artists = json.load(artists_json_file)
 
    success = False
    try:
        for artist in artists:
            db.session.add(Artist(**artist))
        db.session.commit()
        success = True
    except:
        db.session.rollback()
        success=False
    finally:
        db.session.close()

    return success

def init_all(db, Artist, Show, Venue):
    """ load init data from jsons
    """
    db.drop_all()
    db.create_all()

    # init artists:
    init_artists_status = init_artists(db, Artist)
    # init shows:
    # init venues:
    init_venues_status = init_venues(db, Venue)

    print("[Init DB Summary]:")
    print("\t[artists]: {}".format("success" if init_artists_status else "failed"))
    print("\t[venues]: {}".format("success" if init_venues_status else "failed"))
    