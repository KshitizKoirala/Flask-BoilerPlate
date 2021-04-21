import os
from dotenv import load_dotenv, find_dotenv

# Loading the .env file
load_dotenv(find_dotenv())

# This is your Project Root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, '/profile_picture_uploads')
print(ROOT_DIR)


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_CREDENTIALS")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAX_CONTENT_LENGTH = 15 * 1024 * 1024
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
