from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import routes  # this imports routes and registers them to the blueprint
