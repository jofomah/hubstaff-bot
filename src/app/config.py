import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secretsecret')
    HUBSTAFF_APP_TOKEN = os.environ.get('HUBSTAFF_APP_TOKEN')
    HUBSTAFF_API_ACCOUNT_EMAIL = os.environ.get('HUBSTAFF_API_ACCOUNT_EMAIL')
    HUBSTAFF_API_ACCOUNT_PASSWORD = os.environ.get('HUBSTAFF_API_ACCOUNT_PASSWORD')
    HUBSTAFF_AUTH_TOKEN = os.environ.get('HUBSTAFF_AUTH_TOKEN')
    HUBSTAFF_ORGANIZATION_ID = os.environ.get('HUBSTAFF_ORGANIZATION_ID')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'


class TestingConfig(Config):
    TESTING = True
    FLASK_ENV = 'testing'
