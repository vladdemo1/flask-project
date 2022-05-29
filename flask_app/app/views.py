"""
This mod contains main routes in app
"""

from app import app
from flask import json
from sqlalchemy.exc import IntegrityError
from app.main import database
from app.models import user


@app.route("/ping")
def ping():
    """
    Test func about check work app
    """
    return app.response_class(response=json.dumps({'msg': 'pong'}), status=200, mimetype='application/json')


@app.route("/add_user")  # , methods=("POST", "GET")
def add_user():
    """
    Simple func about add user to database
    """
    try:
        # request.form['email'] ...
        # check data about mail or etc
        u = user.User('demodemo140gmail.com', 'vlad', '12345', True)
        database.create_user(u)
    except IntegrityError:
        return app.response_class(response=json.dumps({'msg': 'user is exists'}),
                                  status=400, mimetype='application/json')
    return app.response_class(response=json.dumps({'msg': 'OK'}), status=200, mimetype='application/json')
