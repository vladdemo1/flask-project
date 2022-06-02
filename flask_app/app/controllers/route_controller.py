"""
This mod contains main class RouteController about work in views
"""

import flask_login
from flask_login import logout_user
from sqlalchemy.exc import IntegrityError

from app.main.database_model import DatabaseModel
from app.models.user import User
from app.models.user_login import UserLogin


class RouteController:
    """
    This class responsible about work view and database
    """

    @staticmethod
    def film_paginate(page: int, search_pattern: str, count_film_per_page=10):
        """
        Get films with paginate
        """
        return DatabaseModel().films_paginate_with_pattern(page, count_film_per_page, search_pattern)

    @staticmethod
    def get_all_films(page_number: int, count_per_page=10):
        """
        Get all films from database
        """
        return DatabaseModel().get_all_films(page_number=page_number, count_per_page=count_per_page)

    @staticmethod
    def get_user_password_hash(user_name):
        """
        Get user's password hash
        """
        return User.find_by_name(user_name).password

    @staticmethod
    def get_name_user_login():
        """
        Get name current user who is log in
        """
        return flask_login.current_user.username

    @staticmethod
    def get_id_user(username: str) -> int:
        return DatabaseModel().get_id_user_by_name(username)

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        return DatabaseModel().get_user_by_id(user_id)

    @staticmethod
    def logout_user():
        logout_user()

    @staticmethod
    def add_user_to_database(name: str, email: str, password: str):
        try:
            new_user = User(email=email, name=name, password=password)
            new_user.save_to_db()
        except IntegrityError:
            return 400, {'Message': 'User is exists'}

        return 200, new_user.json()

    @staticmethod
    def get_user_login(name: str, password: str, user_id: int):
        return UserLogin(username=name, password=password, user_id=user_id)
