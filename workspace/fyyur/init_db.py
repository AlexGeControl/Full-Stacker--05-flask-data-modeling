import json

def create_venues(db, Venue):
    # load init venues from json:
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