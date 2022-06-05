"""
This mod contains main class about logging
"""

from flask import current_app
from werkzeug.local import LocalProxy

logger = LocalProxy(lambda: current_app.logger)


class MainLogger:
    """
    Class about logging in app
    """

    def __init__(self, user, method='POST', data=None, route=None, status=200, message=None):
        """
        Make log with parameters
        """
        _user = f"user = {user}"
        _method = f"method = {method}"
        _data = f"data = {data}"
        _route = f"route = {route}"
        _status = f"status = {status}"
        _message = f"message = {message}"

        _text = self._get_message(_user, _method, _data, _route, _status, _message)

        logger.info(_text)

    @staticmethod
    def _get_message(*args):
        """
        Get text for log
        """
        return [val for val in args]
