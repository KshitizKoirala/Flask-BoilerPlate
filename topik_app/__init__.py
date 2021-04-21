from flask import Flask

# Configuration Files
from .extensions import db, ma
from .config.config import DevelopmentConfig
from dotenv import load_dotenv, find_dotenv

# Custom Routes
from .users.routes import users
from .languages.routes import languages


# Loading the .env file
load_dotenv(find_dotenv())


def create_app(config_file=DevelopmentConfig):
    app = Flask(__name__)
    # Configuring and Initializing the respective db of the app using context
    app.config.from_object(config_file)
    with app.app_context():
        db.init_app(app)
        ma.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(languages)
    return app
