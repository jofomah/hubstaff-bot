import flask

from hubstaff import app
from hubstaff.routes import auth
from hubstaff.tests import helper as test_helper


def check_protected_route(route):
    '''tests that route is protected'''

    client = app.test_client()

    # ensure that user is logged out
    test_helper.logout(client)

    response = client.get(route, follow_redirects=True)

    # redirects to login page
    assert b'Login' in response.data


def test_that_index_route_is_protected():
    '''test that the index route is protected'''

    check_protected_route('/')


def test_that_export_report_route_is_protected():
    '''tests that export report route is protected'''

    check_protected_route('/export-report/2019-08-12')


def test_that_logout_route_is_protected():

    client = app.test_client()

    # ensure that user is logged out
    test_helper.logout(client)

    response = client.post('/logout', follow_redirects=True)

    # redirects to login page
    assert b'Login' in response.data


def test_login_with_wrong_crecentials():
    '''test that login guards against wrong credentials'''

    client = app.test_client()

    response = test_helper.login(client, 'invalid@email.com', 'wrongpassword')

    assert b'Please check your login details and try again.' in response.data


def test_load_user_returns_none_for_unknown_user():
    '''tests login manager's load user'''

    unknown_email = 'unknown_guest_user@example.com'

    user = auth.load_user(unknown_email)

    assert user is None


def test_load_user_returns_expected_user():
    '''test that load user returns user if account exists'''

    admin_email = flask.current_app.config.get('ADMIN_EMAIL')

    user = auth.load_user(admin_email)

    assert user is not None
    assert user.email == admin_email
