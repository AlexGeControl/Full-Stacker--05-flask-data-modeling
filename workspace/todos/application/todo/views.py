import sys

from application import db
from application.models import Todo

from flask import render_template, jsonify, request, flash, redirect, url_for

from . import bp

#  ----------------------------------------------------------------
#  routes
#  ----------------------------------------------------------------

#  CREATE
#  ----------------------------------------------------------------
@bp.route('/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    if error:
        abort (400)
    else:
        return jsonify(body)

#  READ
#  ----------------------------------------------------------------

#  UPDATE
#  ----------------------------------------------------------------

#  DELETE
#  ----------------------------------------------------------------