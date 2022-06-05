"""
This mod contains main routes in app
"""

from flask_login import login_required, login_user, current_user
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from app.app import app
from app.app import users_repository

from app.controllers.route_controller import RouteController
from app.logging.logs import MainLogger


@app.route("/ping", methods=['POST'])
def ping():
    """
    Test func about check work app
    """
    if request.method == "POST":
        return jsonify({'msg': 'pong'})


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Login user with flask-login
    """
    if request.method == "POST":
        data = request.get_json()
        user_name = data["name"]
        user_email = data["email"]
        user_password = data["password"]

        if not user_name or not user_email or not user_password:
            return jsonify({'Message': 'User not log in'})

        hash_password = RouteController().get_user_password_hash(user_name=user_name)
        check_passwords = check_password_hash(hash_password, user_password)

        if not check_passwords:
            return jsonify({'Message': 'Password is not correct'})

        user_id = RouteController().get_id_user(username=user_name)

        if user_id is None:
            return jsonify({'Message': 'User is not exists in database'})

        user_from_database = RouteController().get_user_by_id(user_id)

        user_login = RouteController().get_user_login(name=user_from_database.name,
                                                      password=user_from_database.password,
                                                      user_id=users_repository.next_index())

        users_repository.save_user(user_login)
        login_user(user_login)

        del data["password"]
        MainLogger(user=user_name, data=data, route='/login', message="User log in")

        return jsonify({'Message': 'User successfully logged in'})


@app.route('/protected', methods=["POST"])
@login_required
def protected():
    """
    Check about login user
    """
    if request.method == "POST":
        name_user_login = RouteController().get_name_user_login()
        return jsonify({'Message': f'Logged in as :{name_user_login}'})


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register user + add to flask-login
    """
    if request.method == "POST":
        data = request.get_json()

        user_name: str = data["name"]
        user_email: str = data["email"]
        user_password: str = data["password"]
        user_password_too: str = data["password_too"]

        if not user_name:
            return jsonify({'Message': 'Name not field or invalid user name'})

        if not user_email:
            return jsonify({'Message': 'Email not field or invalid email'})

        if not user_password or not user_password_too:
            return jsonify({'Message': 'Password not field'})

        if user_password != user_password_too:
            return jsonify({'Message': 'Passwords are not equal'})

        password_hash = generate_password_hash(user_password)

        message = RouteController().add_user_to_database(name=user_name,
                                                         email=user_email,
                                                         password=password_hash)

        user_login = RouteController().get_user_login(name=user_name,
                                                      password=password_hash,
                                                      user_id=users_repository.next_index())
        users_repository.save_user(user_login)
        login_user(user_login)

        del data["password"]
        del data["password_too"]
        MainLogger(user=user_name, data=data, route='/register', message="User registered")

        return jsonify(message)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    """
    Log out from flask-login
    """
    if request.method == "POST":
        username = current_user.username
        RouteController().logout_user()
        MainLogger(user=username, data=request.get_json(), route='/logout', message="User log out")
        return jsonify({'Message': 'Logout completed'})


@app.route("/films", methods=['GET', 'POST'])
def films():
    """
    Show all films and current search by pattern
    """
    if request.method == 'POST':
        data = request.get_json()
        search_pattern = data['search_pattern']
        number_page = data['number_page']

        if not search_pattern:
            all_films = RouteController().get_all_films(page_number=number_page)
            MainLogger(user=current_user.username, data=data, route='/films', message="Show films without pattern")
            return jsonify({'Films': f'{all_films}'})

        films_with_paginate = RouteController().film_paginate(page=number_page, search_pattern=search_pattern)
        MainLogger(user=current_user.username, data=data, route='/films', message="Show films with pattern")
        return jsonify({'Films': f'{films_with_paginate}'})

    first_films = RouteController().get_all_films(page_number=1)
    return jsonify({'Films': f'{first_films}'})


@app.route("/postman", methods=['GET', 'POST'])
def postman():
    if request.method == "POST":
        data = request.get_json()
        return jsonify({'Your name:': f'{data}'})
