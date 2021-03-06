import os


class CONFIG:
    SECRET_KEY = os.environ["APP_SECRET_KEY"]
    DEBUG = False


class DEVELOPMENT_CONFIG(CONFIG):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TESTING_CONFIG(CONFIG):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ["TEST_DATABASE_URI"]
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class PRODUCTION_CONFIG(CONFIG):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]


configs = dict(
    dev=DEVELOPMENT_CONFIG,
    test=TESTING_CONFIG,
    prod=PRODUCTION_CONFIG
)

key = CONFIG.SECRET_KEY
