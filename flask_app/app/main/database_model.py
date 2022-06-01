"""
This mod contains all logic about work with database
"""

from app.models.film import Film


class DatabaseModel:
    """
    This class contain all functions about work with database
    """

    @staticmethod
    def get_all_films():
        """
        This func can get all films from database return it
        """
        Film.query.all()

    @staticmethod
    def films_paginate_with_pattern(page_number: int, count_per_page: int, pattern: str):
        """
        This func can get films with paginate by current pattern search by name film
        """
        films = Film.query.filter(Film.name.like(pattern + '%'))
        return films.paginate(page=page_number, per_page=count_per_page).items
