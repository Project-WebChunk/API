from flask import Flask, jsonify, request
from dotenv import load_dotenv

import os

from database import Database

if os.path.isfile('.env'):
    load_dotenv('.env')

app = Flask(__name__)
app.config.from_mapping(dict(os.environ))

database = Database()

@app.route('/')
def index():
    return jsonify({'status': 'success', 'version': '0.0.1'})

if __name__ == "__main__":
    app.run(debug=True if os.getenv('ENVIRONMENT') == 'development' else False)