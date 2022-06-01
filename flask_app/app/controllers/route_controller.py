"""
This mod contains main class RouteController about work in views
"""

from app.main.database_model import DatabaseModel


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
    def get_all_films():
        """
        Get all films from database
        """
        return DatabaseModel().get_all_films()
