"""
This mod contains main init about app
"""

import logging
from flask import Flask
from flask_migrate import Migrate


app = Flask(__name__)

migration = Migrate(directory='./app/migrations')

console = logging.getLogger('console')

from app.main.database import init_db

init_db()

from . import views
