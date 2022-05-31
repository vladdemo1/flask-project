"""
This mod contains main init about app
"""

import logging

from flask import Flask
from flask_login import LoginManager

from app.main.database import db, migrate
from app import config
from app.models.user_login import UsersRepository


app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

console = logging.getLogger('console')
login_manager = LoginManager()
login_manager.login_view = 'login'
users_repository = UsersRepository()


@app.before_first_request
def create_all():
    """
    Init database, migrations and login_manager about flask-login
    """
    db.init_app(app)
    migrate.init_app(app, db, directory='migrations')
    db.create_all()

    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """
    Callback to reload the user object
    """
    return users_repository.get_user_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    """
    If user not log in
    """
    return 'Unauthorized', 401
