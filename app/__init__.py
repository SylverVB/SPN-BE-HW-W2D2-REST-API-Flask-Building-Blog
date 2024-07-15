import os
from flask import Flask # Import the Flask class from the flask library
from app.database import db, migrate # Import the instance of SQLAlchemy (db) and instance of Migrate (migrate) from database module
from app.limiter import limiter
from app.caching import cache
from app.swagger_docs import swaggerui_blueprint
from app.models import Role, User
import logging
# import sys


# Create an instance of the flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///advanced_blog_api.db'

# database_url = os.environ.get('DATABASE_URL') or 'sqlite:///advanced_blog_api.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = database_url

# # Log the database URI
# app.logger.info(f'Using database URL: {database_url}')

# Initialize the app with the flask-sqlalchemy
db.init_app(app)

# Initialize the app and db with migrate
migrate.init_app(app, db)

# Initialize the app with flask-limiter
limiter.init_app(app)

# Initialize the app with flask-caching
cache.init_app(app)

# Register the Swagger UI Blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix='/api/docs')

# # Set up logging to stdout and file
# logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("debug.log")])
# app.logger.setLevel(logging.INFO)

# Enable foreign keys for SQLite
@app.before_request
def before_request():
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        from sqlalchemy import event
        from sqlalchemy.engine import Engine

        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

# Import the routes file so that it runs
from . import routes, models  