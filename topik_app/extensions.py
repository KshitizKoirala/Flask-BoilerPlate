from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from authlib.integrations.flask_client import OAuth

# Initialize the database
db = SQLAlchemy()

# Initialize Marshmallow Serializer
ma = Marshmallow()

# Initialize OAuth
oauth = OAuth()

# Initialize Flask-Mail
mail = Mail()
