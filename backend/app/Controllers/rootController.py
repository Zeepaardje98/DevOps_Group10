import os

from flask import request, jsonify
from app import app
import json


@app.route('/', methods=['GET'])
def hello():
    message = "Server is running"
    print(message)
    return jsonify({
        "status": 200,
        "result": {
            "message": message,
            "env": os.environ.get('FLASK_ENV'),
        }
    })
