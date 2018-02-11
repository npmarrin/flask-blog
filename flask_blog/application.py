from flask import Flask
from flask_blog.auth.views import auth as auth_blueprint

from . import db, bcrypt
from .config import DevelopmentConfig


# factory to create the Flask app and initialize extensions
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    db.init_app(app)
    bcrypt.init_app(app)
    return app
