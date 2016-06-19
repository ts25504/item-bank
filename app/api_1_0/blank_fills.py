from flask import jsonify
from app.api_1_0 import api
from app.models import BlankFill


@api.route('/blank_fill/')
def get_all_blank_fill():
    blank_fills = BlankFill.query.all()
    return jsonify(
        {'blank_fills': [bf.to_json()] for bf in blank_fills})


@api.route('/blank_fill/<int:id>')
def get_blank_fill(id):
    blank_fill = BlankFill.query.get_or_404(id)
    return jsonify(blank_fill.to_json())
