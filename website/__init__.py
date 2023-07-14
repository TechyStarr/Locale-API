from flask import Flask
from flask_restx import Api
from website.utils.utils import db
from .api.auth import auth_namespace
from .api.views import view_namespace
from .api.search import search_ns
from website.config.config import config_dict
from website.models.auth import User, ApiKey
from website.models.data import Region, State, Lga, load_dataset
from flask_migrate import Migrate
from website.utils.utils import db, cache, limiter
from flask_jwt_extended import JWTManager, get_jwt
from flask_cors import CORS




def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config) # config object from config.py file in config folder
    # app.config['CACHE_DEFAULT_TIMEOUT'] = 300 # Specify the default cache timeout in seconds (e.g., 300 seconds = 5 minutes)
    # app.config['CACHE_TYPE'] = 'SimpleCache' # Flask-Caching related configs 
    # app.config['CACHE_KEY_PREFIX'] = 'locale' # Specify a prefix for cache keys (optional)
    # app.config['CACHE_THRESHOLD'] = 300 # Specify the maximum number of items to be cached (optional)
    
    # cache = Cache(app, config={'CACHE_TYPE': 'simple'})
    cache.init_app(app)

    # view_namespace.cache = cache
    # search_ns.cache = cache
    # auth_namespace.cache = cache

    # cors = CORS(app, resources={r"/*": {"origins": "https://locale-fe-fgze.onrender.com"}})
    cors = CORS(app)

    limiter.init_app(app) # initialize limiter with app instance to enable rate limiting


    db.init_app(app)

    jwt = JWTManager(app)

    blacklist = set()

    def check_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    # @jwt.expired_token_loader
    # def expired_token_callback(expired_token):
    #     claims = get_jwt()['user_claims']
    #     return ({'message': 'The token has expired'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'message': 'Invalid token'}, 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return {'message': 'Missing or Invalid authorization'}, 401



    migrate = Migrate(app, db)

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize user "
        }
    }


    api = Api(app,
        title="Locale API", 
        description='Find Locations in Nigeria.\n'
            'The API is built with Python, Flask and Flask-RESTX.\n'
            'Follow the steps below to use the API:\n'
            '1. Create a user account\n'
            '2. Login to generate a JWT token\n'
            '3. Add the token to the Authorization header with the Bearer prefix eg "Bearer JWT-token"\n'
            '4. Use the token to access the endpoints',
        version="1.0",
        # prefix="/api/v1",
        authorizations = authorizations,
        security = "Bearer Auth"
    )


    # register namespaces for api
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(view_namespace, path='/view')
    api.add_namespace(search_ns, path='/query')



    @app.shell_context_processor 
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Region': Region,
            'State': State,
            'Lga': Lga,
            'ApiKey': ApiKey
        }

    with app.app_context():
        db.create_all()
    
    return app

