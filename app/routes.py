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


# Lesson 3: Assignment | API Security

# Task 1: Implement JWT Token Generation

# - Add the pyjwt library to the requirements.txt file to enable JWT token generation and validation.
# - Create a utils folder and generate the util.py file to create tokens and validate tokens as required.
# - Define a secret key to be used for signing the JWT tokens.
# - Implement a function named encode_token(user_id) in util.py to generate JWT tokens with an expiration time and user ID as the payload.
# - Ensure that the secret key is kept secure and not exposed publicly.
# - Test the token generation function to ensure that tokens are generated correctly.

# Task 2: Authentication Logic

# - Create a login function to authenticate users using the User model.
# - Utilize the encode_token function from the util.py module to generate the JWT token with the user ID as the payload.
# - Return the JWT token along with a success message upon successful authentication.
# - Create the controller to handle the JWT token returned from the authentication service.

# Task 3: Update Endpoints

# - Update the endpoint to create a post so that it requires a token
# - Utilize the token_auth.login_required function from the auth.py module to verify the token.
# - If the request does not have a token, send a 401 response.

# Expected Outcomes:

# - Implementation of JWT token-based authentication and authorization to enhance the security of the blog.
# - Successful generation of JWT tokens with expiration time and user ID as the payload.
# - Integration of JWT token generation and validation into the authentication logic to provide secure access to endpoints.
# - A more secure blog with JWT token-based authentication, ensuring the protection of sensitive data and resources.



from app import app # from the app folder, import the app variable (Flask instance)
from flask import request
from app.schemas.userSchema import user_input_schema, user_output_schema, users_schema, user_login_schema
from app.schemas.postSchema import post_schema, posts_schema
from marshmallow import ValidationError
from app.database import db
from app.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.util import encode_token
from app.auth import token_auth


@app.route('/')
def index():
    return 'Welcome to the blog!'

# ==== Token Endpoints ====

@app.route('/token', methods=["POST"])
def get_token():
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400 # Bad Request by Client
    try:
        data = request.json
        credentials = user_login_schema.load(data)
        # Query the user table for a user with that username
        query = db.select(User).where(User.username == credentials['username'])
        user = db.session.scalars(query).first()
        # If is is a user and the user's password matches the credentials
        if user is not None and check_password_hash(user.password, credentials['password']):
            # Generate a token with the user's id
            auth_token = encode_token(user.user_id)
            return {'token': auth_token}, 200
        # If either the user with that username does not exist or the password is wrong
        else:
            return {"error": "Username and/or password is incorrect"}, 401 # Unauthorized
    except ValidationError as err:
        return err.messages, 400

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
@token_auth.login_required
def create_post():
    # Check if the request has a JSON body
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400 # Bad Request by Client
    try:
        # Get the request JSON body
        data = request.json
        # Check if the body has all of the required fields
        post_data = post_schema.load(data)

        # Get the current user from the token
        current_user = token_auth.current_user()

        # Create a new instance of Post 
        new_post = Post(
            title=post_data['title'],
            body=post_data['body'],
            # user_id=post_data['user_id']
            # Use the user_id from the authenticated token instead of the request body:
            user_id=current_user.user_id  # Use the user_id from the authenticated user
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