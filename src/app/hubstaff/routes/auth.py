import flask
import flask_login
from werkzeug import security

from hubstaff import app, login_manager
from hubstaff.models.user import User


@login_manager.user_loader
def load_user(user_email):
    _user = User.query.filter(User.email == user_email).first()
    if not _user:
        return None
    return _user


@app.route("/login", methods=['GET', 'POST'])
def login():
    '''Routes for showing login view and processing login request'''

    if flask.request.method == 'GET':
        return flask.render_template('login.html')

    elif flask.request.method == 'POST':
        email = flask.request.form.get('email')
        password = flask.request.form.get('password')
        remember = True if flask.request.form.get('remember') else False

        user = User.get_by(email)

        if not user or not security.check_password_hash(user.password, password):

            flask.flash('Please check your login details and try again.')
            return flask.redirect(flask.url_for('login'))

        flask_login.login_user(user, remember=remember)

        return flask.redirect(flask.url_for('index'))


@app.route('/logout', methods=['POST'])
@flask_login.login_required
def logout():
    '''Logs out current logged in user'''

    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))
