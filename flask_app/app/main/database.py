"""
This mod contains connect to database and main funcs about CRUD
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


url = f"postgresql://{os.environ.get('POSTGRES_USER')}:" \
                                       f"{os.environ.get('POSTGRES_PASSWORD')}@db:5432/" \
                                       f"{os.environ.get('POSTGRES_DB')}"

engine = create_engine(url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """
    Func about init database and import main models
    """
    from app.models import user
    Base.metadata.create_all(bind=engine)


def create_user(user):
    """
    Func about add user to database
    :param user: object user with data
    """
    db_session.add(user)
    # db.session.flush()
    db_session.commit()
