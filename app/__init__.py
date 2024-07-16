import os
from flask import Flask
from app.database import db, migrate
from app.limiter import limiter
from app.caching import cache
from app.swagger_docs import swaggerui_blueprint
from app.models import Role, User
from flask.cli import with_appcontext
import click

# Create an instance of the flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///advanced_blog_api.db'

# database_url = os.environ.get('DATABASE_URL') or 'sqlite:///advanced_blog_api.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = database_url

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

# Import the routes file so that it runs
from . import routes, models

# Import the setup_roles_and_update_users function
from setup_roles import setup_roles_and_update_users

@click.command(name='setup_roles')
@with_appcontext
def setup_roles_command():
    """Command to set up and update roles."""
    setup_roles_and_update_users()

# Add the command to the Flask CLI
app.cli.add_command(setup_roles_command)