from . import db


class Base(db.Model):
    """Convenience base DB model class.

    1. Makes sure tables in MySQL are created as InnoDB.
    2. Make all UTF8 characters are supported
       https://dev.mysql.com/doc/refman/5.7/en/charset-unicode-utf8mb4.html
    """

    __abstract__ = True
    __table_args__ = dict(mysql_charset='utf8mb4', mysql_engine='InnoDB')
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
