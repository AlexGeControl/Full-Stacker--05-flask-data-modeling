from flask import Blueprint

venue = Blueprint('venue', __name__)

from . import forms, views