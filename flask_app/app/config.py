"""
Config main app
"""

from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://{getenv('POSTGRES_USER')}:" \
                                       f"{getenv('POSTGRES_PASSWORD')}@db:5432/" \
                                       f"{getenv('POSTGRES_DB')}"

APP_SECRET_KEY = getenv('APP_SECRET_KEY')

SQLALCHEMY_TRACK_MODIFICATIONS = False
