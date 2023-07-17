from flask_sqlalchemy import SQLAlchemy
from .cache import cache
from flask import Flask
app = Flask(__name__)
from flask_jwt_extended import JWTManager, create_access_token
from datetime import datetime, timedelta
import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


db = SQLAlchemy()
jwt = JWTManager(app)



# rate limit of 100 requests per minute
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    )



def generate_reset_token(user_id):
    # expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    token = create_access_token(identity=user_id)
    return token