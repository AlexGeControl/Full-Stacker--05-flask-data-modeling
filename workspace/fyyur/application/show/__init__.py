from flask import Blueprint

bp = Blueprint('show', __name__)

from . import forms, views