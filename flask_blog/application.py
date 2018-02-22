from flask import Flask

from . import db, bcrypt, csrf
from .config import DevelopmentConfig
from flask_blog.auth.views import auth as auth_blueprint
from flask_blog.api.views import api as api_blueprint


# factory to create the Flask app and initialize extensions
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    return app
