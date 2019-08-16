from flask_login import UserMixin
from werkzeug import security

from hubstaff import db


class User(db.Model, UserMixin):
    '''User model'''

    email = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String(255), nullable=False, default='')
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)

    def __str__(self):
        return self.email

    def get_id(self):
        return self.email

    def is_active(self) -> bool:
        return self.is_enabled

    @staticmethod
    def create_user(email: str, password: str, is_enabled: bool = True) -> str:
        '''Create user'''

        try:
            password_hash = security.generate_password_hash(password)
            _user = User(email=email, is_enabled=is_enabled, password=password_hash)

            db.session.add(_user)
            db.session.commit()
            return _user.email

        except BaseException as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_by(email):
        '''Get user by email if it exists'''

        return User.query.filter(User.email == email).first()
