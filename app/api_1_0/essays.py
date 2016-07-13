from flask import jsonify, request, current_app, url_for
from app.import db
from app.api_1_0 import api
from app.model.essay_model import Essay


@api.route('/essays/')
def get_essays():
    page = request.args.get('page', 1, type=int)
    pagination = Essay.query.paginate(
        page, per_page=current_app.config['QUESTIONS_PER_PAGE'],
        error_out=False)
    essays = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_essays', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_essays', page=page+1, _external=True)
    return jsonify({
        'essays': [es.to_json() for es in essays],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/essays/<int:id>')
def get_essay(id):
    es = Essay.query.get_or_404(id)
    return jsonify(es.to_json())


@api.route('/essays/<int:id>', methods=['PUT'])
def edit_essay(id):
    es = Essay.query.get_or_404(id)
    es.question = request.json.get('question', es.question)
    es.difficult_level = request.json.get(
        'difficult_level', es.difficult_level)
    es.faq = request.json.get('faq', es.faq)
    es.timestamp = request.json.get('timestamp', es.timestamp)
    es.knowledge_points = request.json.get(
        'knowledge_points', es.knowledge_points)
    es.subject = request.json.get('subject', es.subject)
    es.answer = request.json.get('answer', es.answer)
    db.session.add(sc)
    db.session.commit()
    return jsonify(es.to_json())
