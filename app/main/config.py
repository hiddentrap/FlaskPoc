import os

basedir = os.path.abspath(os.path.dirname(__file__))


# oracle_uri = os.envrion['DATABASE_URI']
# oracle_uri = 'oracle://hjj:hjj@cx_Oracle.makedsn(172.168.1.23,1521,xe)'

class Config:
    SECRET_KEY = os.getenv('SCREAT_KEY', 'my_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = oracle_uri
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_IDS_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_IDS_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = oracle_uri


config_by_name = dict(
    dev=DevelopmentConfig
    , test=TestingConfig
    , prod=ProductionConfig
)

key = Config.SECRET_KEY