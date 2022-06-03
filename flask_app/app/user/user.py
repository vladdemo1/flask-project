"""
This mod contains blueprint about route 'films' when user can make something with films
"""

from flask import Blueprint, redirect, request, jsonify
from flask_login import login_required

# from app.controllers.route_controller import RouteController


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

        # user_name = RouteController().get_name_user_login()
        # user_id = RouteController().get_id_user(user_name)
        #
        film_name = data["film_name"]
        # film_genre = data["film_genre"]
        # film_date = data["film_date"]
        # film_director = data["film_director"]
        # film_description = data["film_description"]
        # film_rating = data["film_rating"]
        # film_poster = data["film_poster"]

        # FOR TEST
        if film_name == "BOB":
            return jsonify("FOR TEST"), 200

        # Add next work this func


@user.route("/delete", methods=['GET', 'POST'])
@login_required
def delete_film():
    """
    Delete film by register user or admin
    """
    if request.method == 'POST':
        data = request.get_json()
        user_id = 1  # edit
        admin_status = False  # edit
        film_name = data['film_name']
        film_user_id = 1  # edit

        if user_id != film_user_id or not admin_status:
            return jsonify({"message": "This user cant delete this film"})

        # use RouteController about next move

        return jsonify({"message": f"Film {film_name} deleted"})


@user.route("/edit", methods=['GET', 'POST'])
@login_required
def edit_film():
    """
    Edit film by register user or admin
    """
    if request.method == 'POST':
        data = request.get_json()

        user_id = 1  # edit
        admin_status = False  # edit
        film_name = data['film_name']
        film_user_id = 1  # edit

        # ADD FIELD ABOUT EDIT

        if user_id != film_user_id or not admin_status:
            return redirect(BASE_URL)

        # ADD MODE CHECK DATA INPUT

        # use RouteController about next move

        return jsonify({"message": "film added"})
