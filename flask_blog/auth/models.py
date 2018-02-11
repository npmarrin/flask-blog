from flask_blog import db, bcrypt
from flask_blog.models import Base
from sqlalchemy.dialects.mysql import BINARY


class User(Base):

    __tablename__ = 'users'

    """UK Government Data Standards Catalogue
       http://webarchive.nationalarchives.gov.uk/+/http://www.cabinetoffice.gov.uk/media/254290/GDS%20Catalogue%20Vol%202.pdf"""
    name = db.Column(db.String(70), nullable=False)
    # https://www.rfc-editor.org/errata_search.php?eid=1690
    email = db.Column(db.String(320), unique=True, nullable=False)
    password_hash = db.Column(BINARY(60), nullable=False)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
