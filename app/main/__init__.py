from flask import Blueprint

main = Blueprint('main', __name__)

from app.main import errors
from app.main.views import login_views
from app.main.views import single_choice_views
from app.main.views import blank_fill_views
from app.main.views import essay_views
from app.main.views import subject_views
from app.main.views import point_views
from app.main.views import test_paper_views
from app.main.views import other_views
