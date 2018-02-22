import datetime
import uuid

from . import db


def generate_uuid():
    return uuid.uuid4().hex


class Base(db.Model):
    """Convenience base DB model class.

    1. Makes sure tables in MySQL are created as InnoDB.
    2. Make all UTF8 characters are supported
       https://dev.mysql.com/doc/refman/5.7/en/charset-unicode-utf8mb4.html
    """

    __abstract__ = True
    __table_args__ = dict(
        mysql_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    _id = db.Column(
        'id',
        db.String(32),
        primary_key=True,
        default=generate_uuid
    )
    _created = db.Column(
        'created',
        db.DateTime,
        default=datetime.datetime.now,
        nullable=False
    )
    _last_modified = db.Column(
        'last_modified',
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False
    )

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, model_id):
        raise TypeError('id is not a settable attribute')

    @property
    def created(self):
        return self._created

    @created.setter
    def created(self, model_created):
        raise TypeError('created is not a settable attribute')

    @property
    def last_modified(self):
        return self.last_modified

    @last_modified.setter
    def last_modified(self, model_last_modified):
        raise TypeError('last_modified is not a settable attribute')
