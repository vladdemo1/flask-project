"""
This mod contains main class about model User in database
"""

from sqlalchemy import Integer, String, Boolean
from sqlalchemy_utils import EmailType
from app.main.database import db
from app.models.base_model import BaseModel


class User(db.Model, BaseModel):
    """
    This is a base user model
    """
    __tablename__ = 'user'

    id = db.Column(Integer, primary_key=True, nullable=False)
    email = db.Column(EmailType, nullable=False, unique=True)
    name = db.Column(String(50), nullable=False, unique=True)
    password = db.Column(String(255), nullable=False)
    admin = db.Column(Boolean, nullable=False, default=False)

    def __init__(self, email, name, password, admin=False):
        self.email = email
        self.name = name
        self.password = password
        self.admin = admin

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, admin={self.admin})>"

    def json(self):
        """
        Get info about user in json format
        """
        return {'id': self.id, 'email': self.email, 'name': self.name, 'admin': self.admin}

    @classmethod
    def find_by_name(cls, name):
        """
        Get and return user from database by name
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, user_id):
        """
        Get and return user from database by id
        """
        return cls.query.filter_by(id=user_id).first()
