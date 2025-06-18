# app/stories/__init__.py
from flask import Blueprint

stories = Blueprint('stories', __name__)

from . import routes  # Use relative import AFTER blueprint is created
