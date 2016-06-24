from flask import Blueprint

main = Blueprint('main', __name__)

from app.main import errors
from app.main.views import login_views, single_choice_views, blank_fill_views,\
     essay_views, subject_views, point_views, test_paper_views, other_views
