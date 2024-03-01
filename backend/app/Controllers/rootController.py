from flask import request, jsonify
from app import app
import json


@app.route('/hello', methods=['GET'])
def hello():
    message = "Hello World!"
    print(message)
    return jsonify({
        "status": 200,
        "result": {
            "message": message
        }
    })

# @app.route('/', methods=['GET'])
# def hello():
#     name = json.loads(request.form.get('name'))
#     message = "Hello " + name + "!"
#     return jsonify({
#         "status": 200,
#         "result": {
#             "message": message
#         }
#     })
