from flask import Blueprint

bp = Blueprint('artist', __name__)

from . import forms, views