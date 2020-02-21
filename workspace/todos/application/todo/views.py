import sys

from application import db
from application.models import Todo

from flask import abort, render_template, jsonify, request, flash, redirect, url_for

from . import bp

#  ----------------------------------------------------------------
#  routes
#  ----------------------------------------------------------------

#  CREATE
#  ----------------------------------------------------------------
@bp.route('/create', methods=['POST'])
def create_todo():
    error = False
    res = {}

    try:
        # parse user input -- AJAX:
        description = request.get_json()['description']
        # create todo:
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        # generate response:
        res['description'] = todo.description
        res['completed'] = todo.completed
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    if error:
        abort(400)
    else:
        return jsonify(res)

#  READ
#  ----------------------------------------------------------------
@bp.route('/', methods=['GET'])
def todos():
    todos = [
        todo.to_dict() for todo in Todo.query.all()
    ]

    return jsonify(todos)

#  UPDATE
#  ----------------------------------------------------------------
@bp.route('/<int:todo_id>/edit', methods=['PUT'])
def edit_todo(todo_id):
    error = False
    res = {}

    try:
        # parse user input -- AJAX:
        completed = request.get_json()['completed']

        # read todo:
        todo = Todo.query.get(todo_id)
        # write:
        todo.completed = completed
        # update:
        db.session.add(todo)
        db.session.commit()

        # generate response:
        res['description'] = todo.description
        res['completed'] = todo.completed
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    if error:
        abort(400)
    else:
        return jsonify(res)    

#  DELETE
#  ----------------------------------------------------------------
@bp.route('/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    error = False
    res = {}

    try:
        # identify
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()

        # generate response:
        res["success"] = True
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    if error:
        abort(400)
    else:
        return jsonify(res)