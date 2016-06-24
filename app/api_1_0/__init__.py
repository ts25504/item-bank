from flask import Blueprint

api = Blueprint('api', __name__)

from app.api_1_0 import users, single_choices, blank_fills, essays
