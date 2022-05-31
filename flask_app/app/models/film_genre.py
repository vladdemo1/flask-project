"""
This mod contains main class about model FilmGenre in database
"""

from sqlalchemy import ForeignKey

from app.main.database import db

film_genre = db.Table(
    "film_genre",
    db.Column("film_id", ForeignKey("film.id")),
    db.Column("genre_id", ForeignKey("genre.id")),
)
