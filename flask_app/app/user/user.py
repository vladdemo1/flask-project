"""
This mod contains blueprint about route 'films' when user can make something with films
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.controllers.route_controller import RouteController
from app.logging.logs import MainLogger

user = Blueprint(name='films', import_name=__name__)
BASE_URL = '/films'


@user.route("/add", methods=['GET', 'POST'])
@login_required
def add_film():
    """
    Add film by register user or admin
    """
    if request.method == 'POST':
        data = request.get_json()

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
            return jsonify({"Message": "Incorrect input film name"})

        if len(film_genres) < 1:
            return jsonify({"Message": "Field about film genres is empty"})

        film_genres_id = RouteController().get_genres_id(genres=film_genres)

        film_director_id = RouteController().get_film_director_id(director_name=film_director)

        if film_rating < 0 or film_rating > 10:
            return jsonify({"Message": "Incorrect rating value"})

        if not film_poster:
            return jsonify({"Message": "Field poster is empty"})

        film_id = RouteController().add_film_to_database(name=film_name, date=film_date, rating=film_rating,
                                                         poster=film_poster, description=film_description,
                                                         director_id=film_director_id, user_id=user_id)

        for genre_id in film_genres_id:
            RouteController().add_relation_film_genre(film_id=film_id, genre_id=genre_id)

        MainLogger(user=current_user.username, data=data, route=BASE_URL + '/add', message="Add film by user")
        return jsonify({"Message": f"Film {film_name} added!"})


@user.route("/delete", methods=['GET', 'POST'])
@login_required
def delete_film():
    """
    Delete film by register user or admin
    """
    if request.method == 'POST':
        data = request.get_json()

        user_name = RouteController().get_name_user_login()
        user_id = RouteController().get_id_user(user_name)
        admin_status = RouteController().get_user_admin_status(username=user_name)

        film_name = data['film_name']
        film_user_id = RouteController().get_user_id_by_film(film_name=film_name)

        if not film_user_id:
            return jsonify({"message": "Film not found"})

        if user_id != film_user_id and not admin_status:
            return jsonify({"message": "This user cant delete this film"})

        RouteController().delete_film_by_name(film_name)

        MainLogger(user=current_user.username, data=data, route=BASE_URL + '/delete', message="Film deleted by user")
        return jsonify({"message": f"Film {film_name} deleted"})


@user.route("/edit", methods=['GET', 'POST'])
@login_required
def edit_film():
    """
    Edit film by register user or admin
    """
    if request.method == 'POST':
        data = request.get_json()

        user_name = RouteController().get_name_user_login()
        user_id = RouteController().get_id_user(user_name)
        admin_status = RouteController().get_user_admin_status(username=user_name)

        film_name = data['name']
        film_user_id = RouteController().get_user_id_by_film(film_name=film_name)

        if not film_user_id:
            return jsonify({"message": "Film not found"})

        if user_id != film_user_id and not admin_status:
            return jsonify({"message": "This user cant edit this film"})

        if data['director_id']:
            data['director_id'] = RouteController().get_film_director_id(director_name=data['director_id'])

        RouteController().update_film(film_name, **data)

        MainLogger(user=current_user.username, data=data, route=BASE_URL + '/edit', message="Film edited by user")
        return jsonify({"message": f"Film {film_name} edit"})


@user.route("/sort", methods=['GET', 'POST'])
def sorting_film():
    """
    Sorting film by rating or date
    """
    if request.method == 'POST':
        title = 'Films'

        data = request.get_json()
        number_page = data['number_page']

        if not data['date'] and data['rating']:
            films_sort_by_rating = RouteController().get_films_sort_rating(number_page=number_page)
            return jsonify({f'{title}': f'{films_sort_by_rating}'})

        if not data['rating'] and data['date']:
            films_sort_by_date = RouteController().get_films_sort_date(number_page=number_page)
            return jsonify({f'{title}': f'{films_sort_by_date}'})

        films_multi_sort = RouteController().get_films_sort_multi(number_page=number_page)
        return jsonify({f'{title}': f'{films_multi_sort}'})


@user.route("/filter", methods=['GET', 'POST'])
def filter_film():
    """
    Filter films by genre, dates or director
    """
    if request.method == "POST":
        title = 'Films'

        data = request.get_json()
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
