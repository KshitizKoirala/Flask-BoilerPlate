import os
import pathlib
from dotenv import load_dotenv, find_dotenv

# Loading the .env file
load_dotenv(find_dotenv())

# This is your Project Root
ROOT_DIR = pathlib.Path().absolute()
PROFILE_UPLOAD_FOLDER = f"{ROOT_DIR}\\topik_app\\assets\profile_picture_uploads"
QUESTION_UPLOAD_FOLDER = f"{ROOT_DIR}\\topik_app\\assets\question_image_uploads"


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_CREDENTIALS")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROFILE_UPLOAD_FOLDER = PROFILE_UPLOAD_FOLDER
    QUESTION_UPLOAD_FOLDER = QUESTION_UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 15 * 1024 * 1024
    SECRET_KEY = os.getenv("SECRET_KEY")
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    # Email server
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    # MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("Test_DB_CREDENTIALS")
