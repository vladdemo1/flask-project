"""
This mod contains blueprint about route 'films' when user can make something with films
"""

from flask import Blueprint, redirect


user = Blueprint(name='films', import_name=__name__)
BASE_URL = '/films'


@user.route("/add")
def add_film():
    """
    Add film by register user or admin
    """
    # place for future code
    return redirect(BASE_URL)


@user.route("/delete")
def delete_film():
    """
    Delete film by register user or admin
    """
    # place for future code
    return redirect(BASE_URL)


@user.route("/edit")
def edit_film():
    """
    Edit film by register user or admin
    """
    # place for future code
    return redirect(BASE_URL)
