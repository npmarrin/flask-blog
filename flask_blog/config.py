import os
from urllib.parse import quote_plus

import yaml


DATABASE_YAML = 'database.yml'
ORM_KEY = 'sqlalchemy'


def get_database_uri():
    uri = ''
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), DATABASE_YAML), 'r') as file:
        db_config = yaml.load(file)
        if ORM_KEY in db_config:
            uri = '{driver}://{username}:{password}@{host}/{schema}'.format(
                driver=quote_plus(db_config[ORM_KEY].get('driver', '')),
                username=quote_plus(db_config[ORM_KEY].get('username', '')),
                password=quote_plus(db_config[ORM_KEY].get('password', '')),
                host=quote_plus(db_config[ORM_KEY].get('hostname', '')),
                schema=quote_plus(db_config[ORM_KEY].get('schema', ''))
            )
    return uri


class Config:
    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # https://raw.githubusercontent.com/maxcountryman/flask-bcrypt/master/flask_bcrypt.py
    BCRYPT_HANDLE_LONG_PASSWORDS = True
    BCRYPT_LOG_ROUNDS = 12


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    MAIL_SERVER = 'email'
    MAIL_USERNAME = 'relay@mail.example.com'
    MAIL_PASSWORD = 'relay'
    MAIL_SUPPRESS_SEND = False
    SECRET_KEY = 'd26e1b0ee19b03a7ac98f37e1efe0762ad64f7305356'
