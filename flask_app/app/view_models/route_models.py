"""
This mod contains all models for routes
"""

from app.app import api, fields

test_model = api.model('Test Model', {
    "name": fields.String(default=None),
    "password": fields.String(default=None),
})

login_model = api.model('Login Model', {
    "name": fields.String(default=None),
    "email": fields.String(default=None),
    "password": fields.String(default=None),
})

register_model = api.model('Register Model', {
    "name": fields.String(default=None),
    "email": fields.String(default=None),
    "password": fields.String(default=None),
    "password_too": fields.String(default=None),
})

logout_model = api.model('Log Out Model', {})

films_model = api.model('Films Model', {
    "search_pattern": fields.String(default=None),
    "number_page": fields.Integer(default=None),
})

list_about_genre = api.model('List About Genre', {
    "genre": fields.String(default=None),
})

films_add_model = api.model("Films Add Model", {
    "film_name": fields.String(default=None),
    "film_genre": fields.List(fields.Nested(list_about_genre), default=None),
    "film_date": fields.Date(default=None),
    "film_director": fields.String(default=None),
    "film_description": fields.String(default=None),
    "film_rating": fields.Integer(default=None),
    "film_poster": fields.String(default=None),
})

films_delete_model = api.model('Films Delete Model', {
    "film_name": fields.String(default=None),
})

films_edit_model = api.model('Films Edit Model', {
    "name": fields.String(default=None),
    "date": fields.Date(default=None),
    "rating": fields.Integer(default=None),
    "poster": fields.String(default=None),
    "description": fields.String(default=None),
})

films_sort_model = api.model('Films Sort Model', {
    "number_page": fields.Integer(default=None),
    "date": fields.Date(default=None),
    "rating": fields.Integer(default=None),
})

films_filter_model = api.model('Film Filter Model', {
    "number_page": fields.Integer(default=None),
    "genre": fields.String(default=None),
    "left_date": fields.Date(default=None),
    "right_date": fields.Date(default=None),
    "director": fields.String(default=None),
})
