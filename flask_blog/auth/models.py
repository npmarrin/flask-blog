import datetime

from flask import session
from sqlalchemy.dialects.mysql import BINARY
from jwt import encode as jwt_encode,\
     decode as jwt_decode,\
     ExpiredSignatureError,\
     InvalidTokenError

from flask_blog import db, bcrypt
from flask_blog.models import Base


class User(Base):

    __tablename__ = 'users'

    """UK Government Data Standards Catalogue
       http://webarchive.nationalarchives.gov.uk/+/http://www.cabinetoffice.gov.uk/media/254290/GDS%20Catalogue%20Vol%202.pdf
    """
    name = db.Column(
        db.String(70),
        nullable=False
    )
    # https://www.rfc-editor.org/errata_search.php?eid=1690
    email = db.Column(
        db.String(320),
        unique=True,
        nullable=False
    )
    _password_hash = db.Column(
        'password_hash',
        BINARY(60),
        nullable=False
    )

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    @property
    def password(self):
        raise TypeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            return user

        return None

    def __repr__(self):
        return\
            "<User(id={}, name={}, email={})>".format(
                self.id,
                self.name,
                self.email
            )

    def remember_me_token(self, secret, timedelta, issuer, algorithm='HS256'):
        payload = {
            'exp': datetime.datetime.utcnow() + timedelta,
            'iat': datetime.datetime.utcnow(),
            'iss': issuer,
            'sub': self.id
        }
        return jwt_encode(
            payload,
            secret,
            algorithm=algorithm
        )

    @staticmethod
    def validate_remember_me_token(jwt_token, secret, issuer):
        """
        Decodes the jwt token and validates content
        """
        try:
            payload = jwt_decode(jwt_token, secret)

            user = User.query.filter_by(_id=payload['sub']).first()

            if user is None:
                return False

            payload_time = datetime.datetime.utcfromtimestamp(
                payload.get('exp')
            )

            return\
                payload.get('iss') == issuer and\
                payload.get('sub') == user.id and\
                payload_time > datetime.datetime.utcnow()

        except (ExpiredSignatureError, InvalidTokenError):
            return False

    def set_user_session(self):
        session['user'] = (self.id, self.name, self.email)

    @staticmethod
    def register(name, email, password):
        registrant = User(
            name=name,
            email=email
        )

        registrant.password = password

        db.session.add(registrant)
        db.session.commit()

        registrant.set_user_session()
        return registrant
