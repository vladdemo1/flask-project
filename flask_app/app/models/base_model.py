"""This mod contains main class about functions for models"""
from app.main.database import db


class BaseModel:
    """
    Base class for all models about main func with db
    """

    def save_to_db(self):
        """
        Save obj (something model) to database
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Delete model as obj (something model) from database
        """
        db.session.delete(self)
        db.session.commit()
