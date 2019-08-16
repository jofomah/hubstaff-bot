import os

import flask
import flask_login
import flask_sqlalchemy

import config
from hubstaff.services.client import HubStaff

# create and configure the app
app = flask.Flask(__name__, instance_relative_config=True)
app.app_context().push()

# set config object base on ENV
env = os.environ.get('FLASK_ENV')
if env == 'dev' or env == 'development':
    env_config = config.DevelopmentConfig()
elif env == 'prod' or env == 'production':
    env_config = config.ProductionConfig()
elif env == 'test' or env == 'testing':
    env_config = config.TestingConfig()
else:
    env_config = config.DevelopmentConfig()

app.config.from_object(env_config)


# register SQLAlchemy
db = flask_sqlalchemy.SQLAlchemy()
db.init_app(app)

# register Flask-Login's login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# register flask bootstrap
from flask_bootstrap import Bootstrap  # noqa: F401 E402
Bootstrap(app)

# import routes and models, etc
import hubstaff.routes.auth    # noqa: F401 E402
import hubstaff.routes.index   # noqa: F401 E402
import hubstaff.models.user    # noqa: F401 E402
import hubstaff.utils.filters  # noqa: F401 E402


def generate_auth_token():
    '''Generate auth token automatically'''

    app_token = flask.current_app.config['HUBSTAFF_APP_TOKEN']
    account_email = flask.current_app.config['HUBSTAFF_API_ACCOUNT_EMAIL']
    account_password = flask.current_app.config['HUBSTAFF_API_ACCOUNT_PASSWORD']

    hs_client = HubStaff(app_token)
    hs_client.set_auth_token(account_email, account_password)

    return hs_client.auth_token


@app.before_first_request
def obtain_auth_token_if_not_set():
    '''Obtain HubStaff API v1 auth token if not set'''

    auth_token = flask.current_app.config.get('HUBSTAFF_AUTH_TOKEN')

    # auth token not set yet, obtain and set
    if auth_token is None:
        token = generate_auth_token()
        flask.current_app.config.update(HUBSTAFF_AUTH_TOKEN=token)


@app.before_first_request
def create_admin_user():
    '''Create initial user account, admin account '''

    admin_email = flask.current_app.config.get('ADMIN_EMAIL')
    admin_password = flask.current_app.config.get('ADMIN_PASSWORD')
    is_enabled = True

    if not hubstaff.models.user.User.get_by(admin_email):
        hubstaff.models.user.User.create_user(
            admin_email,
            admin_password, is_enabled
        )
