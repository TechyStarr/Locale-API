import os
from decouple import config
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

db_name = 'localedb'


# default_uri = "postgres://{}:{}@{}/{}".format('postgres', 'starrb15', 'localhost:5432', db_name)

# default_uri = "postgresql://users:ARfVJqF9NIQjO3QIrtiXSZhGPkDGPzrf@dpg-cifuuolph6erq6hlbmag-a.oregon-postgres.render.com/localedb_sjat"

uri = os.getenv('DATABASE_URL', 'default_uri')
if uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=90)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    CACHE_TYPE = 'simple'
    

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # An SQL memory database is used

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = config('DEBUG', False, cast=bool)


config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}

# postgres://users:BB8ud8VkKOiX62lpH2DlmluD6xyS8z0K@dpg-cifd9ap5rnujc4rvos50-a.oregon-postgres.render.com/localedb_wa4b