import logging
import os
from flask import Flask

# future import api
# future import db, migration
# future import logging

app = Flask(__name__)

console = logging.getLogger('console')

# future import models

from . import views
