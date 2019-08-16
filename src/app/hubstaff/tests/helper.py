import flask


def login(client, email=None, password=None):
    '''helper login function'''

    if email is None:
        email = flask.current_app.config.get('ADMIN_EMAIL')

    if password is None:
        password = flask.current_app.config.get('ADMIN_PASSWORD')

    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    '''helper logout function'''

    return client.post('/logout', follow_redirects=True)
