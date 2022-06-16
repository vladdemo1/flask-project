"""
This mod contains main routes in app
"""

from flask_login import login_required, current_user
from flask import request, jsonify

from app.app import api, Resource
from app.controllers.route_controller import RouteController
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

        return jsonify(RouteController().login(data))


@api.route('/register')
@api.expect(route_models.register_model)
class Register(Resource):
    @api.doc(model=route_models.register_model)
    def post(self):
        """
        Register user + add to flask-login
        """
        data = request.get_json(force=True)

        return jsonify(RouteController().register(data))


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
        data = request.get_json(force=True)

        return jsonify(RouteController().logout_user(username, data))


@api.route("/films")
@api.expect(route_models.films_model)
class Films(Resource):
    @api.doc(model=route_models.films_model)
    def post(self):
        """
        Show all films and current search by pattern
        """
        data = request.get_json(force=True)

        return jsonify(RouteController().films(data))


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

        return jsonify(RouteController().film_add(data))


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

        return jsonify(RouteController().film_delete(data))


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

        return jsonify(RouteController().film_edit(data))


@api.route("/films/sort")
@api.expect(route_models.films_sort_model)
class FilmsSort(Resource):
    @api.doc(model=route_models.films_sort_model)
    def post(self):
        """
        Sorting film by rating or date
        """
        data = request.get_json(force=True)

        return jsonify(RouteController().film_sort(data))


@api.route("/films/filter")
@api.expect(route_models.films_filter_model)
class FilmsFilter(Resource):
    @api.doc(model=route_models.films_filter_model)
    def post(self):
        """
        Filter films by genre, dates or director
        """
        data = request.get_json(force=True)

        return jsonify(RouteController().film_filter(data))
