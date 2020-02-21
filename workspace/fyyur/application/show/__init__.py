from flask import Blueprint

show = Blueprint('show', __name__)

from . import forms, views