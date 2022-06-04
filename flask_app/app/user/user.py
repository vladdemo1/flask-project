"""
This mod contains blueprint about route 'films' when user can make something with films
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required

from app.controllers.route_controller import RouteController

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

        return jsonify({"message": f"Film {film_name} edit"})
