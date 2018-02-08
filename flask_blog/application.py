import yaml
import os
from flask import Flask
from flask_blog.extensions import db
from urllib.parse import quote_plus


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


# factory to create the Flask app and initialize extensions
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app
