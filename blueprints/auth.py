from flask import Blueprint, jsonify, request

router = Blueprint('auth', __name__, url_prefix='/auth')

from app import database

@router.route('/register', methods=['POST'])
def register():
    data = request.form
    if "email" not in data:
        return jsonify({'status': 'error', 'message': 'Missing email'}), 400
    if "password" not in data:
        return jsonify({'status': 'error', 'message': 'Missing password'}), 400
    if "username" not in data:
        return jsonify({'status': 'error', 'message': 'Missing username'}), 400

    for value in list(data.values()):
        if value.replace(' ', '') == '' or value == None:
            return jsonify({'status': 'error', 'message': 'Empty value'}), 400

    if database.get_user_by_email(data['email']) != None:
        return jsonify({'status': 'error', 'message': 'Email already exists'}), 400

    if database.get_user(data['username']) != None:
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 400

    user = database.register_user(data['username'], data['email'], data['password'])

    return jsonify({'status': 'success', 'user': user}), 201