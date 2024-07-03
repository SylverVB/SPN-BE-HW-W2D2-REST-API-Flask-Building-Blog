import os
from flask import Flask # Import the Flask class from the flask library
from app.database import db, migrate # Import the instance of SQLAlchemy (db) and instance of Migrate (migrate) from database module


# Create an instance of the flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# Initialize the app with the flask-sqlalchemy
db.init_app(app)

# Initialize the app and db with migrate
migrate.init_app(app, db)

# Import the routes file so that it runs
from . import routes, models  