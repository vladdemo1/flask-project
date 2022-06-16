"""
This mod contains main class RouteController about work in views
"""

import flask_login
from flask_login import logout_user, login_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.main.database_model import DatabaseModel
from app.models.user import User
from app.models.user_login import UserLogin
from app.models.film import Film
from app.logging.logs import MainLogger, FileLogger
from app.app import users_repository


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
        current_user_ = User.find_by_name(user_name)
        if current_user_ is None:
            return None
        return current_user_.password

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
    def logout_user(username, data: dict) -> dict:
        """
        Logout current user from flask-login
        """
        logout_user()
        MainLogger(user=username, data=data, route='/logout', message="User log out")
        return {'Message': 'Logout completed'}

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
            genre = DatabaseModel().get_genre_by_name(genre)
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

    def login(self, data: dict) -> dict:
        """
        Func with logic about route login.
        Login current user
        """
        user_name = data["name"]
        user_email = data["email"]
        user_password = data["password"]

        if not user_name or not user_email or not user_password:
            message = {'Message': 'User not log in'}
            FileLogger(user_name, message)
            return message

        hash_password = self.get_user_password_hash(user_name=user_name)
        if hash_password is None:
            return {'Message': 'User is not exists'}
        check_passwords = check_password_hash(hash_password, user_password)

        if not check_passwords:
            message = {'Message': 'Password is not correct'}
            FileLogger(user_name, message)
            return message

        user_id = self.get_id_user(username=user_name)
        user_from_database = self.get_user_by_id(user_id)

        user_login = self.get_user_login(name=user_from_database.name,
                                         password=user_from_database.password,
                                         user_id=users_repository.next_index())

        users_repository.save_user(user_login)
        login_user(user_login)

        del data["password"]
        MainLogger(user=user_name, data=data, route='/login', message="User log in")

        return {'Message': 'User successfully logged in'}

    def register(self, data: dict) -> dict:
        """
        Func with logic about route register
        Registered new user
        """
        user_name: str = data["name"]
        user_email: str = data["email"]
        user_password: str = data["password"]
        user_password_too: str = data["password_too"]

        if not user_name:
            message = {'Message': 'Name not field or invalid user name'}
            FileLogger(user_name, message)
            return message

        if not user_email:
            message = {'Message': 'Email not field or invalid email'}
            FileLogger(user_name, message)
            return message

        if not user_password or not user_password_too:
            message = {'Message': 'Password not field'}
            FileLogger(user_name, message)
            return message

        if user_password != user_password_too:
            message = {'Message': 'Passwords are not equal'}
            FileLogger(user_name, message)
            return message

        password_hash = generate_password_hash(user_password)

        message = self.add_user_to_database(name=user_name,
                                            email=user_email,
                                            password=password_hash)

        user_login = self.get_user_login(name=user_name,
                                         password=password_hash,
                                         user_id=users_repository.next_index())
        users_repository.save_user(user_login)
        login_user(user_login)

        del data["password"]
        del data["password_too"]
        MainLogger(user=user_name, data=data, route='/register', message="User registered")
        return message

    def films(self, data: dict) -> dict:
        """
        Func with logic about route films
        Get films by pattern and with paginate
        """
        search_pattern = data['search_pattern']
        number_page = data['number_page']

        if not search_pattern:
            all_films = self.get_all_films(page_number=number_page)
            MainLogger(data=data, route='/films', message="Show films without pattern")
            return {'Films': f'{all_films}'}

        films_with_paginate = self.film_paginate(page=number_page, search_pattern=search_pattern)
        MainLogger(data=data, route='/films', message="Show films with pattern")
        return {'Films': f'{films_with_paginate}'}

    def film_add(self, data: dict) -> dict:
        """
        Func with logic about route film_add
        Add current film to database
        """
        user_name = self.get_name_user_login()
        user_id = self.get_id_user(user_name)

        film_name: str = data["film_name"]
        film_genres: list = data["film_genre"]
        film_date = data["film_date"]
        film_director: str = data["film_director"]
        film_description: str = data["film_description"]
        film_rating: int = data["film_rating"]
        film_poster: str = data["film_poster"]

        if not film_name:
            message = {"Message": "Incorrect input film name"}
            FileLogger(user_name, message)
            return message

        if len(film_genres) < 1:
            message = {"Message": "Field about film genres is empty"}
            FileLogger(user_name, message)
            return message

        film_genres_id = self.get_genres_id(genres=film_genres)

        film_director_id = self.get_film_director_id(director_name=film_director)

        if film_rating < 0 or film_rating > 10:
            message = {"Message": "Incorrect rating value"}
            FileLogger(user_name, message)
            return message

        if not film_poster:
            message = {"Message": "Field poster is empty"}
            FileLogger(user_name, message)
            return message

        film_id = self.add_film_to_database(name=film_name, date=film_date, rating=film_rating,
                                            poster=film_poster, description=film_description,
                                            director_id=film_director_id, user_id=user_id)

        for genre_id in film_genres_id:
            self.add_relation_film_genre(film_id=film_id, genre_id=genre_id)

        MainLogger(user=current_user.username, data=data, route='/films/add', message="Add film by user")
        return {"Message": f"Film {film_name} added!"}

    def film_delete(self, data: dict) -> dict:
        """
        Func with logic about route film_add
        Delete current film from database
        """
        user_name = self.get_name_user_login()
        user_id = self.get_id_user(user_name)
        admin_status = self.get_user_admin_status(username=user_name)

        film_name = data['film_name']
        film_user_id = self.get_user_id_by_film(film_name=film_name)

        if not film_user_id:
            message = {"message": "Film not found"}
            FileLogger(user_name, message)
            return message

        if user_id != film_user_id and not admin_status:
            message = {"message": "This user cant delete this film"}
            FileLogger(user_name, message)
            return message

        self.delete_film_by_name(film_name)

        MainLogger(user=current_user.username, data=data, route='/films/delete', message="Film deleted by user")
        return {"message": f"Film {film_name} deleted"}

    def film_edit(self, data: dict) -> dict:
        """
        Func with logic about route film_edit
        Edit film by input values
        """
        user_name = self.get_name_user_login()
        user_id = self.get_id_user(user_name)
        admin_status = self.get_user_admin_status(username=user_name)

        film_name = data['name']
        film_user_id = self.get_user_id_by_film(film_name=film_name)

        if not film_user_id:
            message = {"message": "Film not found"}
            FileLogger(user_name, message)
            return message

        if user_id != film_user_id and not admin_status:
            message = {"message": "This user cant edit this film"}
            FileLogger(user_name, message)
            return message

        if data['director_id']:
            data['director_id'] = self.get_film_director_id(director_name=data['director_id'])

        self.update_film(film_name, **data)

        MainLogger(user=current_user.username, data=data, route='/films/edit', message="Film edited by user")
        return {"message": f"Film {film_name} edit"}

    def film_sort(self, data: dict) -> dict:
        """
        Func with logic about rout film_sort
        Sort films by fields
        """
        title = 'Films'
        number_page = data['number_page']

        if not data['date'] and data['rating']:
            films_sort_by_rating = self.get_films_sort_rating(number_page=number_page)
            return {f'{title}': f'{films_sort_by_rating}'}

        if not data['rating'] and data['date']:
            films_sort_by_date = self.get_films_sort_date(number_page=number_page)
            return {f'{title}': f'{films_sort_by_date}'}

        films_multi_sort = self.get_films_sort_multi(number_page=number_page)
        return {f'{title}': f'{films_multi_sort}'}

    def film_filter(self, data: dict) -> dict:
        """
        Func with logic about route film_filter
        Filter films by fields
        """
        title = 'Films'
        number_page = data['number_page']
        genre = data['genre']
        left_date = data['left_date']
        right_date = data['right_date']
        director = data['director']

        if genre and not left_date and not right_date and not director:
            films_filter_genres = self.get_films_filter_genres(genre=genre, number_page=number_page)
            return {f'{title}': f'{films_filter_genres}'}

        if left_date and right_date and not genre and not director:
            films_in_interval = self.get_films_in_date_interval(left_date=left_date,
                                                                right_date=right_date,
                                                                number_page=number_page)
            return {f'{title}': f'{films_in_interval}'}

        if director and not genre and not left_date and not right_date:
            films_filter_director = self.get_films_filter_director(director=director,
                                                                   number_page=number_page)
            return {f'{title}': f'{films_filter_director}'}

        return {'Message': 'Incorrect data or empty fields'}
