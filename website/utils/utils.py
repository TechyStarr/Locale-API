from flask_sqlalchemy import SQLAlchemy
from .cache import cache
from flask import Flask
app = Flask(__name__)

db = SQLAlchemy()

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# rate limit of 100 requests per minute
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    )