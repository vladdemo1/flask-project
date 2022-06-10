"""
This mod contains main class about logging
"""

from flask import current_app
from werkzeug.local import LocalProxy
import logging

logger = LocalProxy(lambda: current_app.logger)

logging.basicConfig(filename='error.log', level=logging.INFO, filemode='a')
logger_file = logging.getLogger()


class MainLogger:
    """
    Class about logging in app
    """

    def __init__(self, user=None, method='POST', data=None, route=None, status=200, message=None):
        """
        Make log with parameters
        """
        _user = f"user = {user}"
        _method = f"method = {method}"
        _data = f"data = {data}"
        _route = f"route = {route}"
        _status = f"status = {status}"
        _message = f"message = {message}"

        _text = self.get_message(_user, _method, _data, _route, _status, _message)

        logger.info(_text)

    @staticmethod
    def get_message(*args):
        """
        Get text for log
        """
        return [val for val in args]


class FileLogger:
    """
    Class about logging to file
    """

    def __init__(self, user, message=None):
        _user = f'user = {user}'
        _message = message
        _text = MainLogger.get_message(_user, _message)
        logger_file.info(_text)
