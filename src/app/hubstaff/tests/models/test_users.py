import flask

from hubstaff import db
from hubstaff.models.user import User


def test_get_by_returns_expected_user():
    '''test that get_by returns expected user'''

    email = flask.current_app.config.get('ADMIN_EMAIL')
    user = User.get_by(email)

    assert user is not None
    assert user.email == email


def test_that_is_active_returns_is_enabled_value():
    '''test that is_active()  returns same value is is_enabled property'''

    email = flask.current_app.config.get('ADMIN_EMAIL')
    user = User.get_by(email)

    assert user.is_enabled == user.is_active()


def test_that_get_id_returns_expected_value():
    '''test that get_id matches user email'''

    email = flask.current_app.config.get('ADMIN_EMAIL')
    user = User.get_by(email)

    assert user.email == user.get_id()


def test_create_user_enabled_by_default():
    '''test that create user, creates user'''

    email = 'test1234743383@example.com'
    password = 'test4321'

    user_email = User.create_user(email, password)

    user = User.get_by(email)

    assert email == user_email
    assert user.is_enabled is True

    db.session.delete(user)
    db.session.commit()


def test_create_user_not_enabled():
    '''test that create user, creates user'''

    email = 'test12346558570890@example.com'
    password = 'test43217'
    is_enabled = False

    user_email = User.create_user(email, password, is_enabled)

    user = User.get_by(email)

    assert email == user_email
    assert user.is_enabled is False
    assert user.is_active() == user.is_enabled

    db.session.delete(user)
    db.session.commit()
