"""
This mod contains all logic about work with database
"""

from sqlalchemy import update

from app.main.database import db

from app.models.film import Film
from app.models.user import User
from app.models.genre import Genre
from app.models.director import Director
from app.models.film_genre import film_genre


class DatabaseModel:
    """
    This class contain all functions about work with database
    """

    @staticmethod
    def get_all_films(page_number: int, count_per_page: int):
        """
        This func can get all films from database return it
        """
        return Film.query.paginate(page=page_number, per_page=count_per_page).items

    @staticmethod
    def films_paginate_with_pattern(page_number: int, count_per_page: int, pattern: str):
        """
        This func can get films with paginate by current pattern search by name film
        """
        films = Film.query.filter(Film.name.like(pattern + '%'))
        return films.paginate(page=page_number, per_page=count_per_page).items

    @staticmethod
    def get_id_user_by_name(user_name: str) -> int:
        """
        Get id current user by username from database
        """
        user = User.query.filter(User.name == user_name).first()
        return user.id

    @staticmethod
    def get_user_by_id(user_id: int):
        """
        Get User from database by id
        """
        return User.query.filter(User.id == user_id).first()

    @staticmethod
    def get_genre_by_name(genre_name: str):
        """
        Get genre by name
        """
        return Genre.query.filter(Genre.genre == genre_name).first()

    @staticmethod
    def get_director_by_name(director_name: str):
        """
        Get director by name
        """
        return Director.query.filter(Director.name == director_name).first()

    @staticmethod
    def add_to_relation_film_genre(film_id: int, genre_id: int):
        """
        Add custom relation with film and genre in database
        """
        statement = film_genre.insert().values(film_id=film_id, genre_id=genre_id)
        db.session.execute(statement)
        db.session.commit()

    @staticmethod
    def get_user_admin_status(username: str) -> bool:
        """
        Get admin status about current user by username from database
        """
        user = User.query.filter(User.name == username).first()
        return user.admin

    @staticmethod
    def get_film_by_name(film_name: str) -> Film:
        """
        Get film by film name
        """
        return Film.query.filter(Film.name == film_name).first()

    @staticmethod
    def update_film(film_name: str, **kwargs):
        """
        Update film by film name
        """
        stmt = update(Film).where(Film.name == film_name).values(**kwargs). \
            execution_options(synchronize_session="fetch")
        db.session.execute(stmt)
        db.session.commit()

    @staticmethod
    def get_films_sort_rating(page_number: int, count_per_page: int):
        """
        Get films with paginate sort desc by rating
        """
        films = Film.query.order_by(Film.rating.desc())
        return films.paginate(page=page_number, per_page=count_per_page).items

    @staticmethod
    def get_films_sort_date(page_number: int, count_per_page: int):
        """
        Get films with paginate sort desc by date
        """
        films = Film.query.order_by(Film.date.desc())
        return films.paginate(page=page_number, per_page=count_per_page).items

    @staticmethod
    def get_films_sort_multi(page_number: int, count_per_page: int):
        """
        Get films with paginate sort by rating & date
        """
        films = Film.query.order_by(Film.rating.desc(), Film.date.desc())
        return films.paginate(page=page_number, per_page=count_per_page).items

    @staticmethod
    def get_films_filter_genre(genre: str, page_number: int, count_per_page: int):
        """
        Get films with paginate filter by genre
        """
        films = Film.query.filter(Film.genre_id).filter(Genre.genre == genre)

        return films.paginate(page=page_number, per_page=count_per_page).items

    @staticmethod
    def get_films_in_date_interval(left_date, right_date, page_number: int, count_per_page: int):
        """
        Get films with paginate in date interval
        """
        films = Film.query.filter(Film.date > left_date).filter(Film.date < right_date)
        return films.paginate(page=page_number, per_page=count_per_page).items

    @staticmethod
    def get_films_filter_director(director_name: str, page_number: int, count_per_page: int):
        """
        Get films with paginate filter by director
        """
        films = db.session.query(Film, Director
                                 ).filter(Film.director_id == Director.id
                                          ).filter(Director.name == director_name)
        return films.paginate(page=page_number, per_page=count_per_page).items
