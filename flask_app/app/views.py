"""
This mod contains main routes in app
"""

import flask_login
from flask import redirect, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

from app.app import app
from app.models.user_login import UserLogin
from app.models.user import User
from app.app import users_repository

from app.answers.json_answer import JsonAnswer


@app.route("/ping")
def ping():
    """
    Test func about check work app
    """
    return JsonAnswer(current_app=app, status=200, dict_msg={'msg': 'pong'}).return_answer


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Login user with flask-login
    """
    user_name = 'vlad'  # request.form.get('name')
    user_email = 'me@gmail.com'  # request.form.get('email')
    user_password = '12345'  # request.form.get('password')

    if user_name and user_email and user_password:

        registered_user = users_repository.get_user(user_name)
        hash_password = User.find_by_name(user_name).password

        true_pass = check_password_hash(hash_password, user_password)

        if registered_user is not None and true_pass:
            login_user(registered_user)

            return redirect(url_for('protected'))
        else:
            return JsonAnswer(app, 403, {'Message': 'Password is not correct'}).return_answer
    else:
        return JsonAnswer(app, 401, {'Message': 'User not log in'}).return_answer


@app.route('/protected')
@flask_login.login_required
def protected():
    """
    Check about login user
    """
    return JsonAnswer(app, 200, {'Message': f'Logged in as + id:{flask_login.current_user.id}'}).return_answer


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register user + add to flask-login
    """
    user_name = 'vlad'  # request.form.get('name')
    user_email = 'me@gmail.com'  # request.form.get('email')
    user_password = '12345'  # request.form.get('password')
    user_password_too = '12345'  # request.form.get('password_too')
    q = 5
    if q == 5:  # request.method == "POST"
        if not (user_name or user_email or user_password or user_password_too):
            return JsonAnswer(app, 403, {'Message': 'Input all data'}).return_answer

        if user_password != user_password_too:
            return JsonAnswer(app, 403, {'Message': 'Passwords are not equal'}).return_answer

        password_hash = generate_password_hash(user_password)
        try:
            new_user = User(email=user_email, name=user_name, password=password_hash)
            new_user.save_to_db()

            user_login = UserLogin(username=user_name, password=password_hash,
                                   user_id=users_repository.next_index())
            users_repository.save_user(user_login)

        except IntegrityError:
            return JsonAnswer(app, 400, {'Message': 'User is exists'}).return_answer

        return JsonAnswer(app, 200, new_user.json()).return_answer

    return JsonAnswer(app, 401, {'Message': 'Go back to register'}).return_answer


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    """
    Log out from flask-login
    """
    logout_user()
