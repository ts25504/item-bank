from flask import jsonify
from app.api_1_0 import api
from app.model.models import SingleChoice


@api.route('/single_choice/')
def get_all_single_choice():
    single_choices = SingleChoice.query.all()
    return jsonify(
        {'single_choices': [sc.to_json()] for sc in single_choices})


@api.route('/single_choice/<int:id>')
def get_single_choice(id):
    single_choice = SingleChoice.query.get_or_404(id)
    return jsonify(single_choice.to_json())
