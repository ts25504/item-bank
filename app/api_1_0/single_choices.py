from flask import jsonify, request, current_app, url_for
from app import db
from app.api_1_0 import api
from app.model.single_choice_model import SingleChoice


@api.route('/single_choices/')
def get_single_choices():
    page = request.args.get('page', 1, type=int)
    pagination = SingleChoice.query.paginate(
        page, per_page=current_app.config['QUESTIONS_PER_PAGE'],
        error_out=False)
    single_choices = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_single_choices', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_single_choices', page=page+1, _external=True)
    return jsonify({
        'single_choices': [sc.to_json() for sc in single_choices],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/single_choices/<int:id>')
def get_single_choice(id):
    sc = SingleChoice.query.get_or_404(id)
    return jsonify(sc.to_json())


@api.route('/single_choices/<int:id>', methods=['PUT'])
def edit_single_choice(id):
    sc = SingleChoice.query.get_or_404(id)
    sc.question = request.json.get('question', sc.question)
    sc.difficult_level = request.json.get(
        'difficult_level', sc.difficult_level)
    sc.faq = request.json.get('faq', sc.faq)
    sc.subject_id = request.json.get('subject', sc.subject_id)
    sc.points_id = request.json.get('points', sc.points_id)
    sc.answer = request.json.get('answer', sc.answer)
    sc.A = request.json.get('A', sc.A)
    sc.B = request.json.get('B', sc.B)
    sc.C = request.json.get('C', sc.C)
    sc.D = request.json.get('D', sc.D)
    db.session.add(sc)
    db.session.commit()
    return jsonify(sc.to_json())


@api.route('/single_choices/', methods=['POST'])
def new_single_choice():
    sc = SingleChoice()
    sc.question = request.json.get('question', sc.question)
    sc.difficult_level = request.json.get(
        'difficult_level', sc.difficult_level)
    sc.faq = request.json.get('faq', sc.faq)
    sc.subject_id = request.json.get('subject', sc.subject_id)
    sc.points_id = request.json.get('points', sc.points_id)
    sc.answer = request.json.get('answer', sc.answer)
    sc.A = request.json.get('A', sc.A)
    sc.B = request.json.get('B', sc.B)
    sc.C = request.json.get('C', sc.C)
    sc.D = request.json.get('D', sc.D)
    db.session.add(sc)
    db.session.commit()
    return jsonify(sc.to_json()), 201, {'Location': url_for(
        'api.get_single_choice', id=sc.id, _external=True)}


@api.route('/single_choices/<int:id>', methods=['DELETE'])
def delete_single_choice(id):
    sc = SingleChoice.query.get_or_404(id)
    db.session.delete(sc)
    db.session.commit()
    return jsonify(sc.to_json()), 204
