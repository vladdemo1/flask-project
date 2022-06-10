"""
This mod contains main routes in app
"""

from flask_login import login_required, login_user, current_user
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from app.app import api, Resource
from app.app import users_repository

from app.controllers.route_controller import RouteController
from app.logging.logs import MainLogger, FileLogger
from app.view_models import route_models


@api.route('/login')
@api.expect(route_models.login_model)
class Login(Resource):
    @api.doc(model=route_models.login_model)
    def post(self):
        """
        Log in user
        """
        data = request.get_json(force=True)
        user_name = data["name"]
        user_email = data["email"]
        user_password = data["password"]

        if not user_name or not user_email or not user_password:
            message = {'Message': 'User not log in'}
            FileLogger(user_name, message)
            return jsonify(message)

        hash_password = RouteController().get_user_password_hash(user_name=user_name)
        if not hash_password:
            return jsonify({'Message': 'User is not exists'})
        check_passwords = check_password_hash(hash_password, user_password)

        if not check_passwords:
            message = {'Message': 'Password is not correct'}
            FileLogger(user_name, message)
            return jsonify(message)

        user_id = RouteController().get_id_user(username=user_name)
        user_from_database = RouteController().get_user_by_id(user_id)

        user_login = RouteController().get_user_login(name=user_from_database.name,
                                                      password=user_from_database.password,
                                                      user_id=users_repository.next_index())

        users_repository.save_user(user_login)
        login_user(user_login)

        del data["password"]
        MainLogger(user=user_name, data=data, route='/login', message="User log in")

        return jsonify({'Message': 'User successfully logged in'})


@api.route('/register')
@api.expect(route_models.register_model)
class Register(Resource):
    @api.doc(model=route_models.register_model)
    def post(self):
        """
        Register user + add to flask-login
        """
        data = request.get_json(force=True)

        user_name: str = data["name"]
        user_email: str = data["email"]
        user_password: str = data["password"]
        user_password_too: str = data["password_too"]

        if not user_name:
            message = {'Message': 'Name not field or invalid user name'}
            FileLogger(user_name, message)
            return jsonify(message)

        if not user_email:
            message = {'Message': 'Email not field or invalid email'}
            FileLogger(user_name, message)
            return jsonify(message)

        if not user_password or not user_password_too:
            message = {'Message': 'Password not field'}
            FileLogger(user_name, message)
            return jsonify(message)

        if user_password != user_password_too:
            message = {'Message': 'Passwords are not equal'}
            FileLogger(user_name, message)
            return jsonify(message)

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


@api.route("/logout")
@api.expect(route_models.logout_model)
class LogOut(Resource):
    @api.doc(model=route_models.logout_model)
    @login_required
    def post(self):
        """
        Log out from flask-login
        """
        username = current_user.username
        RouteController().logout_user()
        MainLogger(user=username, data=request.get_json(force=True), route='/logout', message="User log out")
        return jsonify({'Message': 'Logout completed'})


@api.route("/films")
@api.expect(route_models.films_model)
class Films(Resource):
    @api.doc(model=route_models.films_model)
    def post(self):
        """
        Show all films and current search by pattern
        """
        data = request.get_json(force=True)
        search_pattern = data['search_pattern']
        number_page = data['number_page']

        if not search_pattern:
            all_films = RouteController().get_all_films(page_number=number_page)
            MainLogger(data=data, route='/films', message="Show films without pattern")
            return jsonify({'Films': f'{all_films}'})

        films_with_paginate = RouteController().film_paginate(page=number_page, search_pattern=search_pattern)
        MainLogger(data=data, route='/films', message="Show films with pattern")
        return jsonify({'Films': f'{films_with_paginate}'})


@api.route("/films/add")
@api.expect(route_models.films_add_model)
class FilmsAdd(Resource):
    @api.doc(model=route_models.films_add_model)
    @login_required
    def post(self):
        """
        Add film by register user or admin
        """
        data = request.get_json(force=True)

        user_name = RouteController().get_name_user_login()
        user_id = RouteController().get_id_user(user_name)

        film_name: str = data["film_name"]
        film_genres: list = data["film_genre"]
        film_date = data["film_date"]
        film_director: str = data["film_director"]
        film_description: str = data["film_description"]
        film_rating: int = data["film_rating"]
        film_poster: str = data["film_poster"]

        if not film_name:
            message = {"Message": "Incorrect input film name"}
            FileLogger(user_name, message)
            return jsonify(message)

        if len(film_genres) < 1:
            message = {"Message": "Field about film genres is empty"}
            FileLogger(user_name, message)
            return jsonify(message)

        film_genres_id = RouteController().get_genres_id(genres=film_genres)

        film_director_id = RouteController().get_film_director_id(director_name=film_director)

        if film_rating < 0 or film_rating > 10:
            message = {"Message": "Incorrect rating value"}
            FileLogger(user_name, message)
            return jsonify(message)

        if not film_poster:
            message = {"Message": "Field poster is empty"}
            FileLogger(user_name, message)
            return jsonify(message)

        film_id = RouteController().add_film_to_database(name=film_name, date=film_date, rating=film_rating,
                                                         poster=film_poster, description=film_description,
                                                         director_id=film_director_id, user_id=user_id)

        for genre_id in film_genres_id:
            RouteController().add_relation_film_genre(film_id=film_id, genre_id=genre_id)

        MainLogger(user=current_user.username, data=data, route='/films/add', message="Add film by user")
        return jsonify({"Message": f"Film {film_name} added!"})


@api.route("/films/delete")
@api.expect(route_models.films_delete_model)
class FilmsDelete(Resource):
    @api.doc(model=route_models.films_delete_model)
    @login_required
    def post(self):
        """
        Delete film by register user or admin
        """
        data = request.get_json(force=True)

        user_name = RouteController().get_name_user_login()
        user_id = RouteController().get_id_user(user_name)
        admin_status = RouteController().get_user_admin_status(username=user_name)

        film_name = data['film_name']
        film_user_id = RouteController().get_user_id_by_film(film_name=film_name)

        if not film_user_id:
            message = {"message": "Film not found"}
            FileLogger(user_name, message)
            return jsonify(message)

        if user_id != film_user_id and not admin_status:
            message = {"message": "This user cant delete this film"}
            FileLogger(user_name, message)
            return jsonify(message)

        RouteController().delete_film_by_name(film_name)

        MainLogger(user=current_user.username, data=data, route='/films/delete', message="Film deleted by user")
        return jsonify({"message": f"Film {film_name} deleted"})


@api.route("/films/edit")
@api.expect(route_models.films_edit_model)
class FilmsEdit(Resource):
    @api.doc(model=route_models.films_edit_model)
    @login_required
    def post(self):
        """
        Edit film by register user or admin
        """
        data = request.get_json(force=True)

        user_name = RouteController().get_name_user_login()
        user_id = RouteController().get_id_user(user_name)
        admin_status = RouteController().get_user_admin_status(username=user_name)

        film_name = data['name']
        film_user_id = RouteController().get_user_id_by_film(film_name=film_name)

        if not film_user_id:
            message = {"message": "Film not found"}
            FileLogger(user_name, message)
            return jsonify(message)

        if user_id != film_user_id and not admin_status:
            message = {"message": "This user cant edit this film"}
            FileLogger(user_name, message)
            return jsonify(message)

        if data['director_id']:
            data['director_id'] = RouteController().get_film_director_id(director_name=data['director_id'])

        RouteController().update_film(film_name, **data)

        MainLogger(user=current_user.username, data=data, route='/films/edit', message="Film edited by user")
        return jsonify({"message": f"Film {film_name} edit"})


@api.route("/films/sort")
@api.expect(route_models.films_sort_model)
class FilmsSort(Resource):
    @api.doc(model=route_models.films_sort_model)
    def post(self):
        """
        Sorting film by rating or date
        """
        title = 'Films'

        data = request.get_json(force=True)
        number_page = data['number_page']

        if not data['date'] and data['rating']:
            films_sort_by_rating = RouteController().get_films_sort_rating(number_page=number_page)
            return jsonify({f'{title}': f'{films_sort_by_rating}'})

        if not data['rating'] and data['date']:
            films_sort_by_date = RouteController().get_films_sort_date(number_page=number_page)
            return jsonify({f'{title}': f'{films_sort_by_date}'})

        films_multi_sort = RouteController().get_films_sort_multi(number_page=number_page)
        return jsonify({f'{title}': f'{films_multi_sort}'})


@api.route("/films/filter")
@api.expect(route_models.films_filter_model)
class FilmsFilter(Resource):
    @api.doc(model=route_models.films_filter_model)
    def post(self):
        """
        Filter films by genre, dates or director
        """
        title = 'Films'

        data = request.get_json(force=True)
        number_page = data['number_page']
        genre = data['genre']
        left_date = data['left_date']
        right_date = data['right_date']
        director = data['director']

        if genre:
            films_filter_genres = RouteController().get_films_filter_genres(genre=genre, number_page=number_page)
            return jsonify({f'{title}': f'{films_filter_genres}'})

        if left_date and right_date:
            films_in_interval = RouteController().get_films_in_date_interval(left_date=left_date,
                                                                             right_date=right_date,
                                                                             number_page=number_page)
            return jsonify({f'{title}': f'{films_in_interval}'})

        if director:
            films_filter_director = RouteController().get_films_filter_director(director=director,
                                                                                number_page=number_page)
            return jsonify({f'{title}': f'{films_filter_director}'})

        return jsonify({'Message': 'Incorrect data or empty fields'})
