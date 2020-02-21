from flask import Blueprint

bp = Blueprint('venue', __name__)

from . import forms, views