"""
This mod in progress ...
about migrations
"""

import logging
from logging.config import fileConfig
import os

from alembic import context

config = context.config

fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

from flask import current_app

config.set_main_option(os.environ.get('DATABASE_URL'),
                       str(current_app.extensions['migrate'].db.engine.url).replace('%', '%%'))
target_metadata = current_app.extensions['migrate'].db.metadata


def run_migrations_offline():

    url = config.get_main_option(os.environ.get('DATABASE_URL'))
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

# add run_migrations_online()


if context.is_offline_mode():
    run_migrations_offline()
# else:
#    run_migrations_online()
