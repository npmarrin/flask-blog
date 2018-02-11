"""Flask and other extensions instantiated here.
"""

from logging import getLogger

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.event import listens_for
from sqlalchemy.pool import Pool
from flask_wtf.csrf import CSRFProtect

LOG = getLogger(__name__)


@listens_for(Pool, 'connect', named=True)
def _on_connect(dbapi_connection, **_):
    """Set MySQL mode to TRADITIONAL on databases that don't set this automatically.

    Without this, MySQL will silently insert invalid values in the database, causing very long debugging sessions in the
    long run.
    http://www.enricozini.org/2012/tips/sa-sqlmode-traditional/
    https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html#sqlmode_traditional
    """

    LOG.debug('Setting SQL Mode to TRADITIONAL.')
    dbapi_connection.cursor().execute("SET SESSION sql_mode='TRADITIONAL'")


db = SQLAlchemy()
bcrypt = Bcrypt()
csrf = CSRFProtect()
