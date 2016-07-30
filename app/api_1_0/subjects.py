from flask import jsonify, request, current_app, url_for
from app import db
from app.api_1_0 import api
from app.model.subject_model import Subject


@api.route('/subjects/')
def get_subjects():
    subjects = Subject.query.all()
    return jsonify({'subjects': [s.to_json() for s in subjects]})


@api.route('/subjects/<int:id>')
def get_subject(id):
    subject = Subject.query.get_or_404(id)
    return jsonify(subject.to_json())


@api.route('/subjects/<int:id>', methods=['PUT'])
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    subject.name = request.json.get('name', subject.name)
    db.session.add(subject)
    db.session.commit()
    return jsonify(subject.to_json())


@api.route('/subjects/', methods=['POST'])
def new_subject():
    subject = Subject()
    subject.name = request.json.get('name', subject.name)
    db.session.add(subject)
    db.session.commit()
    return jsonify(subject.to_json()), 201, {'Location': url_for(
        'api.get_subject', id=subject.id, _external=True)}


@api.route('/subjects/<int:id>', methods=['DELETE'])
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    return jsonify(subject.to_json()), 204
