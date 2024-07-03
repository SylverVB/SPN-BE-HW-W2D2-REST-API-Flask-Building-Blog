# Lesson 1: Assignment | REST API Design Patterns

# Building a Blog with Flask

# Objective: The aim of this assignment is to develop a blog using Flask, incorporating Flask-SQLAlchemy and Flask-Migrate.

# Problem Statement: You are tasked with building a blog API that can handle various aspects of blog operations, including creating, retrieving, and updating users and posts. You can use the following for your models (feel free to modify how you see fit):

# class User(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(db.String(255), nullable=False)
#     username: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
#     email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
#     password: Mapped[str] = mapped_column(db.String(255), nullable=False)

# class Post(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(db.String(255), nullable=False)
#     body: Mapped[str] = mapped_column(db.String)
#     user_id: Mapped[str] = mapped_column(db.Integer, nullable=False)

# Task 1: Implement Flask Application

# - Configure the Flask application using the app package to enable easy configuration and instantiation of the application.
# - Organize the application structure into modules for better code organization and maintainability.

# Task 2: Create Endpoints for CR(UD) Operations

# - For each model (User, Post), create endpoints for performing Create and Fetching All operations.
# - Use the REST Resource Naming Conventions to design the endpoint URLs and methods.
# - Ensure that the endpoints adhere to the principles of RESTful API design, including the use of nouns for resource names, plural nouns for collection names, hyphens to separate words, and lowercase letters.

# Expected Outcomes:

# - Successful implementation of the Flask application allowing for users of the API to "sign up" and create a new User in the database, create new blog posts, and retrieve that data
# - Creation of endpoints for Create and List All operations for each model in the blog system, following the principles of RESTful API design and adhering to REST Resource Naming Conventions.


from app import app # from the app folder, import the app variable (Flask instance)
from flask import request
from app.schemas.userSchema import user_input_schema, user_output_schema, users_schema
from app.schemas.postSchema import post_schema, posts_schema
from marshmallow import ValidationError
from app.database import db
from app.models import User, Post
from werkzeug.security import generate_password_hash


@app.route('/')
def index():
    return 'Welcome to the blog!'

# ==== Users Endpoints ====

# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    query = db.select(User) # select the User model
    users = db.session.execute(query).scalars().all()
    return users_schema.jsonify(users)

# Get a single user by ID
@app.route('/users/<int:user_id>', methods=["GET"])
def get_single_user(user_id):
    user = db.session.get(User, user_id)
    # Check if we get a user back or None
    if user is not None:
        return user_output_schema.jsonify(user)
    return {"error": f"User with ID {user_id} does not exist"}, 404 # Not Found

# Create a new user
@app.route('/users', methods=["POST"])
def create_user():
    # Check if the request has a JSON body
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400 # Bad Request by Client
    try:
        # Get the request JSON body
        data = request.json
        # Check if the body has all of the required fields
        user_data = user_input_schema.load(data)
        # Query the user table to see if any users have that username or email
        query = db.select(User).where( (User.username == user_data['username']) | (User.email == user_data['email']) )
        check_users = db.session.scalars(query).all()
        if check_users: # If there are users in the check_users list (empty list evaluates to false)
            return {"error": "User with that username and/or email already exists"}, 400 # Bad Request by Client

        # Create a new instance of User 
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            email=user_data['email'],
            password=generate_password_hash(user_data['password'])
        )
        # and add to the database
        db.session.add(new_user)
        db.session.commit()
        
        # Serialize the new user object and return with 201 status
        return user_output_schema.jsonify(new_user), 201 # Created - Success
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400


# ==== Posts Endpoints ====

# Get all posts
@app.route('/posts', methods=["GET"])
def get_all_posts():
    query = db.select(Post)
    posts = db.session.scalars(query).all()
    return posts_schema.jsonify(posts)   

# Get a single post by ID
@app.route('/posts/<int:post_id>', methods=["GET"])
def get_single_post(post_id):
    # Search the database for a product with that ID
    post = db.session.get(Post, post_id)
    # Check if we get a post back or None
    if post is not None:
        return post_schema.jsonify(post)
    return {"error": f"Post with ID {post_id} does not exist"}, 404 # Not Found

# Create a new post
@app.route('/posts', methods=["POST"])
def create_post():
    # Check if the request has a JSON body
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400 # Bad Request by Client
    try:
        # Get the request JSON body
        data = request.json
        # Check if the body has all of the required fields
        post_data = post_schema.load(data)

        # Create a new instance of Post 
        new_post = Post(
            title=post_data['title'],
            body=post_data['body'],
            user_id=post_data['user_id']
        )
        # and add to the database
        db.session.add(new_post)
        db.session.commit()
        
        # Serialize the new post object and return with 201 status
        return post_schema.jsonify(new_post), 201 # Created - Success
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400