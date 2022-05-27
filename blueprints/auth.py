from flask import Blueprint, jsonify, request
import jwt

import os

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

@router.route('/verify', methods=['GET'])
def verify():
    try:
        token = request.args.get('token')
        user_id = jwt.decode(token, os.getenv('TOKEN'), algorithms=['HS256'])['_id']
        user = database.get_user_by_id(user_id)
        if user == None:
            return '<div align="center"><font size="6">Oops, User Not Found!</font><br></div>'
        if user['is_verified'] == True:
            return jsonify({'status': 'error', 'message': 'User already verified'}), 400
        database.verify_user(user['_id'])
        return '<div align="center"><font size="6">Yay! You have been verified!</font><br></div>'
    except Exception as e:
        return f'<div align="center"><font size="6">Oops, Something went wrong!</font><br>{str(e)}</div><br>'

@router.route('/login', methods=['POST'])
def login():
    data = request.form
    if "email" not in data:
        return jsonify({'status': 'error', 'message': 'Missing email'}), 400
    if "password" not in data:
        return jsonify({'status': 'error', 'message': 'Missing password'}), 400

    for value in list(data.values()):
        if value.replace(' ', '') == '' or value == None:
            return jsonify({'status': 'error', 'message': 'Empty value'}), 400

    user = database.authenticate_user(data['email'], data['password'])
    if type(user) == str:
        return jsonify({'status': 'error', 'message': user}), 400
    return jsonify({'status': 'success', 'data': user}), 200