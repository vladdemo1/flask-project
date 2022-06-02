"""
This mod contains all logic about work with database
"""

from app.models.film import Film
from app.models.user import User


class DatabaseModel:
    """
    This class contain all functions about work with database
    """

    @staticmethod
    def get_all_films(page_number: int, count_per_page: int):
        """
        This func can get all films from database return it
        """
        films = Film.query.all()
        return films.paginate(page=page_number, per_page=count_per_page).items

    @staticmethod
    def films_paginate_with_pattern(page_number: int, count_per_page: int, pattern: str):
        """
        This func can get films with paginate by current pattern search by name film
        """
        films = Film.query.filter(Film.name.like(pattern + '%'))
        return films.paginate(page=page_number, per_page=count_per_page).items

    @staticmethod
    def get_id_user_by_name(user_name: str) -> int:
        user = User.query.filter(User.name == user_name).first()
        return user.id

    @staticmethod
    def get_user_by_id(user_id: int):
        return User.query.filter(User.id == user_id).first()
