"""
This mod contains main class about user login
"""

from flask_login import UserMixin


class UserLogin(UserMixin):
    """
    User about flask log in
    """

    def __init__(self, username, password, user_id, active=True):
        self.id = user_id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        """
        Get user login id
        """
        return self.id

    def is_active(self):
        """
        Get current user active about login
        """
        return self.active


class UsersRepository:
    """
    Contains all log in users
    """

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0

    def save_user(self, user):
        """
        Save user to repository where all login users
        """
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    def get_user(self, username):
        """
        Get current user (log in) by username
        """
        return self.users.get(username)

    def get_user_by_id(self, userid):
        """
        Get current user (log in) by id
        """
        return self.users_id_dict.get(userid)

    def next_index(self):
        """
        Set next id in repository users log in
        """
        self.identifier += 1
        return self.identifier
