from flask import jsonify, request, current_app, url_for
from app.api_1_0 import api
from app.model.blank_fill_model import BlankFill


@api.route('/blank_fills/')
def get_blank_fills():
    page = request.args.get('page', 1, type=int)
    pagination = BlankFill.query.paginate(
        page, per_page=current_app.config['QUESTIONS_PER_PAGE'],
        error_out=False)
    blank_fills = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_blank_fills', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_blank_fills', page=page+1, _external=True)
    return jsonify({
        'blank_fills': [bf.to_json() for bf in blank_fills],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/blank_fills/<int:id>')
def get_blank_fill(id):
    bf = BlankFill.query.get_or_404(id)
    return jsonify(bf.to_json())


@api.route('/blank_fills/<int:id>', methods=['PUT'])
def edit_blank_fill(id):
    bf = BlankFill.query.get_or_404(id)
    bf.question = request.json.get('question', bf.question)
    bf.difficult_level = request.json.get(
        'difficult_level', bf.difficult_level)
    bf.faq = request.json.get('faq', bf.faq)
    bf.timestamp = request.json.get('timestamp', bf.timestamp)
    bf.knowledge_points = request.json.get(
        'knowledge_points', bf.knowledge_points)
    bf.subject = request.json.get('subject', bf.subject)
    bf.answer = request.json.get('answer', bf.answer)
    return jsonify(bf.to_json())
