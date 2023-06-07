from flask import Flask
from flask_restx import Api
from website.utils.utils import db
from .api.users import auth_namespace
from .api.views import view_namespace
from .webviews.users import auth
from .webviews.views import views
from .api.search import search_ns
from website.config.config import config_dict
from website.models.users import User
from website.models.data import Region, State, Lga, Area
from flask_migrate import Migrate
from flask_login import LoginManager
# from flask_caching import Cache
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager




def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    # cache = Cache(app)

    # limiter = Limiter(app, key_func=get_remote_address)

    # @limiter.limit("100/minute")  # Rate li


    app.config.from_object(config)
    app.config['CACHE_TYPE'] = 'simple'


    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    # authorizations = {
    #     "Bearer Auth": {
    #     "type": "apikey",
    #     "in": "header",
    #     "name": "Authorization", 
    #     "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize user "
    #     }
    # }



    
    # register blueprints for web views
    app.register_blueprint(views, url_prefix='')
    app.register_blueprint(auth, url_prefix='/auth')

    api = Api(app,
    doc="/docs",
    title="Locale API", 
    description="Find whatever you're looking for using Locale",
    # authorization = authorizations,
    # security = "Bearer Auth"
)

    # register namespaces for api
    api.add_namespace(auth_namespace, path='/user')
    api.add_namespace(view_namespace, path='/search')
    api.add_namespace(search_ns, path='/query')







    @app.shell_context_processor 
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Region': Region,
            'State': State,
            'Lga': Lga,
            'Area': Area
        }
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    





    return app

