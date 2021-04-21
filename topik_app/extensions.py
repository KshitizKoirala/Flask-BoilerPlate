from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize the database
db = SQLAlchemy()

# Initialize Marshmallow Serializer
ma = Marshmallow()
