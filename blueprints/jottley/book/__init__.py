from flask import Blueprint, jsonify, request
import jwt

import os

router = Blueprint('book', __name__, url_prefix='/book')

from app import database

@router.route('/', methods=['GET'])
def jottley_book_home():
    return jsonify({'status': 'success', 'version': '0.0.1'})