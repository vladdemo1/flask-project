"""
This mod contains main class RouteController about work in views
"""

import flask_login
from flask_login import logout_user
from sqlalchemy.exc import IntegrityError

from app.main.database_model import DatabaseModel
from app.models.user import User
from app.models.user_login import UserLogin
from app.models.film import Film


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
        current_user = User.find_by_name(user_name)
        if current_user is None:
            return False
        return current_user.password

    @staticmethod
    def get_name_user_login():
        """
        Get name current user who is log in
        """
        return flask_login.current_user.username

    @staticmethod
    def get_id_user(username: str) -> int:
        """
        Get id user by username from database
        """
        return DatabaseModel().get_id_user_by_name(username)

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """
        Get user from database by id
        """
        return DatabaseModel().get_user_by_id(user_id)

    @staticmethod
    def get_user_admin_status(username: str) -> bool:
        """
        Get user admin status from database
        True - real admin
        """
        return DatabaseModel().get_user_admin_status(username)

    @staticmethod
    def logout_user():
        """
        Logout current user from flask-login
        """
        logout_user()

    @staticmethod
    def add_user_to_database(name: str, email: str, password: str):
        """
        Add current user to database
        """
        try:
            new_user = User(email=email, name=name, password=password)
            new_user.save_to_db()
        except IntegrityError:
            return {'Message': 'User is exists'}

        return new_user.json()

    @staticmethod
    def get_user_login(name: str, password: str, user_id: int) -> UserLogin:
        """
        Get current UserLogin
        """
        return UserLogin(username=name, password=password, user_id=user_id)

    @staticmethod
    def get_genres_id(genres: list) -> list:
        """
        Get list genres id by list genres names from database
        """
        genres_id = []
        for genre in genres:
            genre = DatabaseModel().get_genre_by_name(genre['genre'])
            if genre is None:
                genre = DatabaseModel().get_genre_by_name("Unknown")
            genres_id.append(genre.id)

        return genres_id

    @staticmethod
    def get_film_director_id(director_name: str) -> int:
        """
        Get current director id by his name
        """
        current_director = DatabaseModel().get_director_by_name(director_name=director_name)
        if current_director is None:
            current_director = DatabaseModel().get_director_by_name("Unknown")
        return current_director.id

    @staticmethod
    def add_film_to_database(name, date, rating, poster, description, director_id, user_id) -> int:
        """
        Add film to database and return film id
        """
        new_film = Film(name=name, date=date, rating=rating, poster=poster,
                        description=description, director_id=director_id,
                        user_id=user_id)
        new_film.save_to_db()
        return new_film.id

    @staticmethod
    def add_relation_film_genre(film_id: int, genre_id: int):
        """
        Add all custom relations with current film and genres
        """
        DatabaseModel().add_to_relation_film_genre(film_id=film_id, genre_id=genre_id)

    @staticmethod
    def get_user_id_by_film(film_name: str) -> int:
        """
        Get id user by film name from database
        """
        film = DatabaseModel().get_film_by_name(film_name)
        if film is None:
            return False
        return film.user_id

    @staticmethod
    def delete_film_by_name(film_name: str):
        """
        Delete film from database by film name
        """
        film_to_delete = DatabaseModel().get_film_by_name(film_name)
        film_to_delete.delete_from_db()

    @staticmethod
    def update_film(film_name: str, **kwargs):
        """
        Update film by film name
        """
        DatabaseModel().update_film(film_name, **kwargs)

    @staticmethod
    def get_films_sort_rating(number_page: int, count_per_page=10):
        """
        Get films with paginate from database by rating desc sort
        """
        return DatabaseModel().get_films_sort_rating(page_number=number_page, count_per_page=count_per_page)

    @staticmethod
    def get_films_sort_date(number_page: int, count_per_page=10):
        """
        Get films with paginate from database by date desc sort
        """
        return DatabaseModel().get_films_sort_date(page_number=number_page, count_per_page=count_per_page)

    @staticmethod
    def get_films_sort_multi(number_page: int, count_per_page=10):
        """
        Get films with paginate from database by rating & date desc sort
        """
        return DatabaseModel().get_films_sort_multi(page_number=number_page, count_per_page=count_per_page)

    @staticmethod
    def get_films_filter_genres(genre: str, number_page: int, count_per_page=10):
        """
        Get films with paginate from database filer by genre
        """
        return DatabaseModel().get_films_filter_genre(genre=genre, page_number=number_page,
                                                      count_per_page=count_per_page)

    @staticmethod
    def get_films_in_date_interval(left_date, right_date, number_page: int, count_per_page=10):
        """
        Get films with paginate in date interval
        """
        return DatabaseModel().get_films_in_date_interval(left_date=left_date, right_date=right_date,
                                                          page_number=number_page, count_per_page=count_per_page)

    @staticmethod
    def get_films_filter_director(director: str, number_page: int, count_per_page=10):
        """
        Get films with paginate filter by director
        """
        return DatabaseModel().get_films_filter_director(director_name=director, page_number=number_page,
                                                         count_per_page=count_per_page)
