from flask_blog.extensions import db


class Base(db.Model):
    """Convenience base DB model class.

    1. Makes sure tables in MySQL are created as InnoDB.
    2. Make all UTF8 characters are supported
       https://dev.mysql.com/doc/refman/5.7/en/charset-unicode-utf8mb4.html
    """

    __abstract__ = True
    __table_args__ = dict(mysql_charset='utf8mb4', mysql_engine='InnoDB')
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class User(Base):

    __tablename__ = 'users'

    """UK Government Data Standards Catalogue
       http://webarchive.nationalarchives.gov.uk/+/http://www.cabinetoffice.gov.uk/media/254290/GDS%20Catalogue%20Vol%202.pdf"""
    name = db.Column(db.String(70), nullable=False)
    # https://en.wikipedia.org/wiki/Email_address
    email = db.Column(db.String(319), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, name=None, email=None, password=None, role=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
