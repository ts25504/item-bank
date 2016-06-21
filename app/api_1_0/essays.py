from flask import jsonify
from app.api_1_0 import api
from app.model.essay_model import Essay


@api.route('/essay/')
def get_all_essay():
    essays = Essay.query.all()
    return jsonify(
        {'essays': [es.to_json()] for es in essays})


@api.route('/essay/<int:id>')
def get_essay(id):
    essay = Essay.query.get_or_404(id)
    return jsonify(essay.to_json())
