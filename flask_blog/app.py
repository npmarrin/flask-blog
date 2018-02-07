import yaml
import os
from flask import Flask
from flask_blog.extensions import db


DATABASE_YAML = 'database.yml'
CERT_FILE = '/etc/ssl/certs/ssl-cert-snakeoil.pem'
PKEY_FILE = '/etc/ssl/private/ssl-cert-snakeoil.key'

# TODO: This belongs in extension.py
def get_database_uri():
    uri = ''
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),DATABASE_YAML), 'r') as file:
        db_config = yaml.load(file)
        uri = '{driver}://{username}:{password}@{host}/{schema}'.format(
            driver=db_config.get('driver', ''),
            username=db_config.get('username', ''),
            password=db_config.get('password', ''),
            host=db_config.get('lost', ''),
            schema=db_config.get('schema', '')
        )
    return uri


# factory to create the Flask app and initialize extensions
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
    db.init_app(app)
    return app


app = create_app()


@app.route('/')
def hello():
    return 'Hello World! Now'


if __name__ == "__main__":
    # http://werkzeug.pocoo.org/docs/0.14/serving/
    app.run(
        host="0.0.0.0",
        debug=True,
        ssl_context=(CERT_FILE, PKEY_FILE)
    )
