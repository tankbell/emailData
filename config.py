import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('APP_SECRET_KEY', None)
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProdConfiguration(Configuration):
    DEBUG = False

class DevConfiguration(Configuration):
    DEVELOPMENT = True
    DEBUG = True
