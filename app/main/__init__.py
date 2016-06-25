from flask import Blueprint

main = Blueprint('main', __name__)

from app.main import index_views, single_choice_views, blank_fill_views,\
     essay_views, subject_views, point_views, test_paper_views, other_views, \
     errors
