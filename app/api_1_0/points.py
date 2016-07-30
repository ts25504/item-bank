from flask import jsonify, request, url_for
from app import db
from app.api_1_0 import api
from app.model.point_model import Points


@api.route('/points/')
def get_points():
    points = Points.query.all()
    return jsonify({'points': [p.to_json() for p in points]})


@api.route('/points/<int:id>')
def get_point(id):
    point = Points.query.get_or_404(id)
    return jsonify(point.to_json())


@api.route('/points/<int:id>', methods=['PUT'])
def edit_point(id):
    point = Points.query.get_or_404(id)
    point.name = request.json.get('name', point.name)
    point.subject_id = request.json.get('subject', point.subject_id)
    db.session.add(point)
    db.session.commit()
    return jsonify(point.to_json())


@api.route('/points/', methods=['POST'])
def new_point():
    point = Points()
    point.name = request.json.get('name', point.name)
    point.subject_id = request.json.get('subject', point.subject_id)
    db.session.add(point)
    db.session.commit()
    return jsonify(point.to_json()), 201, {'Location': url_for(
        'api.get_point', id=point.id, _external=True)}


@api.route('/points/<int:id>', methods=['DELETE'])
def delete_point(id):
    point = Points.query.get_or_404(id)
    db.session.delete(point)
    db.session.commit()
    return jsonify(point.to_json()), 204
