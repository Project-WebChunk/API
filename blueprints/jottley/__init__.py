from flask import Blueprint, jsonify, request
import jwt

import os

router = Blueprint('jottley', __name__, url_prefix='/jottley')

from app import database
from blueprints.jottley.book import router as book_router

router.register_blueprint(book_router)

@router.route('/', methods=['GET'])
def jottley_home():
    return jsonify({'status': 'success', 'version': '0.0.1'})