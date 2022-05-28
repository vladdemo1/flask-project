from app import app
from flask import json


@app.route("/ping")
def ping():
    return app.response_class(response=json.dumps({'msg': 'pong'}), status=200, mimetype='application/json')
