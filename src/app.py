from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'status': 'success', 'version': '0.0.1'})

if __name__ == "__main__":
    app.run(debug=True)