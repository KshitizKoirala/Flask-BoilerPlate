from flask import Flask
from flask_cors import CORS

# Configuration Files
from .extensions import db, ma, oauth, mail
from .config.config import DevelopmentConfig
from dotenv import load_dotenv, find_dotenv

# Custom Routes
from .api.users.seeder import seeder_bp
from .api.users.routes import users
from .api.languages.routes import languages


# Loading the .env file
load_dotenv(find_dotenv())


def create_app(config_file=DevelopmentConfig):
    app = Flask(__name__)

    # Configuring and Initializing the respective db of the app using context
    app.config.from_object(config_file)
    CORS(app)
    with app.app_context():
        db.init_app(app)
        ma.init_app(app)
        oauth.init_app(app)
        mail.init_app(app)

    app.register_blueprint(seeder_bp)
    app.register_blueprint(users)
    app.register_blueprint(languages)
    return app
