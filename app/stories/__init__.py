"""Stories blueprint."""
from flask import Blueprint

stories = Blueprint('stories', __name__)

from app.stories import routes