from flask import jsonify
from app.api_1_0 import api
from app.model.user_model import User


@api.route('/users/')
def get_users():
    users = User.query.all()
    return jsonify(
        {'users': [u.to_json()] for u in users})

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())
