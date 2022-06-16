"""
This mod contains main tests about current api
"""

from os import getenv
import random
from dotenv import load_dotenv
import pytest
import requests

load_dotenv()
BASE_URL = getenv('BASE_URL')


@pytest.fixture
def normal_data():
    """
    Get random name and email
    """
    random_number = random.randint(1, 1000)
    return f'vlad{random_number}', f'demo{random_number}@gmail.com'


@pytest.fixture
def data():
    """
    Get current normal data about user for registration
    """
    return dict(name="vlad", email="demo@gmail.com", password="12345", password_too="12345")


@pytest.fixture
def data_vladdemo():
    """
    Get current data user for login
    """
    return dict(name="vlad", email="demo@gmail.com", password="12345")


def test_register(data, normal_data):
    """
    Testing rout about register user
    """
    url = f'{BASE_URL}/register'

    data['name'] = ''
    response = requests.post(url, json=data)
    assert response.json() == {'Message': 'Name not field or invalid user name'}
    data['name'] = 'vlad'

    data['email'] = ''
    response = requests.post(url, json=data)
    assert response.json() == {'Message': 'Email not field or invalid email'}
    data['email'] = 'demo@gmail.com'

    data['password'] = ''
    response = requests.post(url, json=data)
    assert response.json() == {'Message': 'Password not field'}
    data['password'] = '12345'

    data['password_too'] = ''
    response = requests.post(url, json=data)
    assert response.json() == {'Message': 'Password not field'}
    data['password_too'] = '55555'

    response = requests.post(url, json=data)
    assert response.json() == {'Message': 'Passwords are not equal'}
    data['password_too'] = '12345'

    data['name'] = normal_data[0]
    data['email'] = normal_data[1]
    response = requests.post(url, json=data)
    assert response.status_code == 200

    response = requests.post(url, json=data)
    assert response.json() == {'Message': 'User is exists'}


def test_login(data):
    """
    Test about login user
    """
    url = f'{BASE_URL}/login'

    data['name'] = 'someone'
    response = requests.post(url, json=data)
    assert response.json() == {'Message': 'User is not exists'}

    data['name'] = ''
    response = requests.post(url, json=data)
    assert response.json() == {'Message': 'User not log in'}
    data['name'] = 'vlad'

    data['password'] = '55555'
    response = requests.post(url, json=data)
    assert response.json() == {'Message': 'Password is not correct'}
    data['password'] = '12345'


def test_normal_login(data):
    """
    Test login with correct data
    """
    url = f'{BASE_URL}/login'
    response = requests.post(url, json=data)
    assert response.json() == {'Message': 'User successfully logged in'}


def test_logout(data_vladdemo):
    """
    Test about logout after login user
    """
    sos = requests.session()

    sos.post(f'{BASE_URL}/login', json=data_vladdemo,
             allow_redirects=True)
    result = sos.post(f'{BASE_URL}/logout', json={})
    print(result.json())


def test_films():
    """
    Test get films with pattern and paginate
    """
    data = {"search_pattern": "New film 2", "number_page": 1}
    url = f'{BASE_URL}/films'
    response = requests.post(url, json=data)
    assert response.json() == {
        "Films": "[<Film(id=2, name=New film 2, director_id=1, user_id=31, genre_id=[<Genre(id=1, genre=Unknown)>])>]"}

    data['search_pattern'] = 'Someone'
    response = requests.post(url, json=data)
    assert response.json() == {'Films': '[]'}

    new_data = {"search_pattern": "", "number_page": 2}
    response = requests.post(url, json=new_data)
    assert response.json() == {
        "Films": "[<Film(id=11, name=Film page 2, director_id=1, user_id=31, genre_id=[<Genre(id=2, genre=Comedian)>])>]"}


def test_films_sort():
    """
    Test about sort films by fields
    """
    data = {"number_page": 2, "date": "2020-06-11", "rating": 10}
    url = f'{BASE_URL}/films/sort'
    response = requests.post(url, json=data)
    assert response.json() == {
        "Films": "[<Film(id=3, name=New film 3, director_id=1, user_id=31, genre_id=[<Genre(id=2, genre=Comedian)>])>]"}

    data["rating"] = ""
    response = requests.post(url, json=data)
    assert response.json() == {
        'Films': '[<Film(id=2, name=New film 2, director_id=1, user_id=31, genre_id=[<Genre(id=1, genre=Unknown)>])>]'}


def test_films_filter():
    """
    Test films filter by genre and date and director
    """
    url = f'{BASE_URL}/films/filter'
    data = {"number_page": 1, "genre": "Comedian", "left_date": "", "right_date": "", "director": ""}
    response = requests.post(url, json=data)
    assert response.json() == {'Films': '[<Film(id=1, name=New film, director_id=2, user_id=31, '
                                        'genre_id=[<Genre(id=2, genre=Comedian)>])>, <Film(id=3, name=New '
                                        'film 3, director_id=1, user_id=31, genre_id=[<Genre(id=2, '
                                        'genre=Comedian)>])>, <Film(id=11, name=Film page 2, director_id=1, '
                                        'user_id=31, genre_id=[<Genre(id=2, genre=Comedian)>])>, '
                                        '<Film(id=12, name=Vlad Demo, director_id=3, user_id=31, '
                                        'genre_id=[<Genre(id=2, genre=Comedian)>])>]'}

    data["genre"] = ''
    data['left_date'] = '2010-01-01'
    data['right_date'] = '2015-01-01'
    response = requests.post(url, json=data)
    assert response.json() == {'Films': '[<Film(id=2, name=New film 2, director_id=1, user_id=31, '
                                        'genre_id=[<Genre(id=1, genre=Unknown)>])>]'}

    data_new = {"number_page": 1, "genre": "", "left_date": "", "right_date": "", "director": "Vlados"}
    response = requests.post(url, json=data_new)
    assert response.json() == {'Films': '[(<Film(id=12, name=Vlad Demo, director_id=3, user_id=31, '
                                        'genre_id=[<Genre(id=2, genre=Comedian)>])>, <Director(id=3, '
                                        'name=Vlados)>)]'}


@pytest.fixture
def vladdemo_session(data_vladdemo):
    """
    Get current session for login required in something routs
    """
    sos = requests.session()
    sos.post(f'{BASE_URL}/login', json=data_vladdemo,
             allow_redirects=True)
    return sos


@pytest.fixture
def film_dict():
    """
    Get normal dict for films add
    """
    return dict(film_name="Test Film", film_genre={"genre": "Unknown"}, film_date="2022-06-11", film_director="Boss",
                film_description="string", film_rating=10, film_poster="string")


URL_FILMS_ADD = f'{BASE_URL}/films/add'


def test_films_add_name(vladdemo_session, film_dict):
    """
    Test about incorrect input data film name
    """
    data = film_dict
    data['film_name'] = ''
    add_films = vladdemo_session.post(URL_FILMS_ADD, json=data)
    assert add_films.json() == {"Message": "Incorrect input film name"}
    data['film_name'] = 'Test Film'


def test_films_add_rating(vladdemo_session, film_dict):
    """
    Test about incorrect input data film rating
    """
    data = film_dict
    data['film_rating'] = 99
    add_films = vladdemo_session.post(URL_FILMS_ADD, json=data)
    assert add_films.json() == {"Message": "Incorrect rating value"}
    data['film_rating'] = 10


def test_films_add_poster(vladdemo_session, film_dict):
    """
    Test about incorrect input data film poster
    """
    data = film_dict
    data['film_poster'] = ""
    add_films = vladdemo_session.post(URL_FILMS_ADD, json=data)
    assert add_films.json() == {"Message": "Field poster is empty"}
    data['film_poster'] = "@vladdemo"


def test_films_add_normal(vladdemo_session, film_dict):
    """
    Test about normal film add
    """
    data = film_dict
    add_films = vladdemo_session.post(URL_FILMS_ADD, json=data)
    assert add_films.json() == {"Message": f"Film {data['film_name']} added!"}


def test_delete_film(vladdemo_session):
    """
    Test about film delete
    """
    url = f'{BASE_URL}/films/delete'
    data = {'film_name': "Someone film"}

    delete_film = vladdemo_session.post(url, json=data)
    assert delete_film.json() == {"message": "Film not found"}

    data['film_name'] = 'Agent'
    delete_film = vladdemo_session.post(url, json=data)
    assert delete_film.json() == {"message": "This user cant delete this film"}

    data['film_name'] = 'Test Film'
    delete_film = vladdemo_session.post(url, json=data)
    assert delete_film.json() == {"message": f"Film {data['film_name']} deleted"}


@pytest.fixture
def data_film_edit():
    """
    Get normal data for film editing
    """
    return {"name": "Agent", "date": "2022-06-11", "rating": 10, "poster": "string", "description": "string"}


def test_edit_film(vladdemo_session, data_film_edit):
    """
    Test about edit film
    """
    url = f'{BASE_URL}/films/edit'
    data = data_film_edit

    edit_film = vladdemo_session.post(url, json=data)
    assert edit_film.json() == {"message": "This user cant edit this film"}

    data['name'] = 'Some one films'
    edit_film = vladdemo_session.post(url, json=data)
    assert edit_film.json() == {"message": "Film not found"}
    data['name'] = "Vlad Demo"

    edit_film = vladdemo_session.post(url, json=data)
    assert edit_film.json() == {"message": f"Film {data['name']} edit"}
