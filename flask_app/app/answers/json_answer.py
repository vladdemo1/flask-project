"""
This mod contains class JsonAnswer with return app.response_class
"""

from flask import json

from app.app import app


class JsonAnswer:
    """
    Get json answer with current status code and message in dict
    """

    def __init__(self, current_app: app, status: int, dict_msg: dict):
        self._app = current_app
        self._status = status
        self._dict_msg = dict_msg
        self._return_answer = self._get_answer()

    @property
    def return_answer(self):
        """
        Get current answer with status code + dict message as json
        """
        return self._return_answer

    def _get_answer(self):
        """
        Create and return answer to app
        """
        return self._app.response_class(response=json.dumps(self._dict_msg),
                                        status=self._status, mimetype='application/json')
