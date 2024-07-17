from app import app, db, limiter, cache # from the app folder, import the app variable (Flask instance)
from flask import request, jsonify, redirect, url_for
from app.schemas.userSchema import user_input_schema, user_output_schema, users_schema, user_login_schema
from app.schemas.postSchema import post_schema, posts_schema
from app.schemas.commentSchema import comment_schema, comments_schema
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
# from app.database import db
from app.models import User, Post, Comment, Role
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.util import encode_token
from app.auth import token_auth, get_roles
import logging
# import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
@limiter.limit("100 per day")
def index():
    # return 'Welcome to the blog!'
    return redirect(url_for('swagger_ui.show'))

# ==== Token Endpoints ====

@app.route('/token', methods=["POST"])
@limiter.limit("100 per day")
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

# Get all users (Admin Only)
@app.route('/users', methods=['GET'])
@token_auth.login_required(role='admin')
@limiter.limit("100 per day")
@cache.cached(timeout=60)
def get_all_users():
    # app.logger.info("Entering get_all_users")
    # sys.stdout.flush()
    # Get any request query params aka request.args
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    query = db.select(User).limit(per_page).offset((page-1)*per_page) # select the User model, limit per page and offset
    users = db.session.execute(query).scalars().all()
    # app.logger.info(f"Fetched comments: {users}")
    # sys.stdout.flush()
    return users_schema.jsonify(users)

# Get a single user by ID (Admin Only)
@app.route('/users/<int:user_id>', methods=["GET"])
@token_auth.login_required(role='admin')
@limiter.limit("100 per day")
@cache.cached(timeout=60)
def get_single_user(user_id):
    user = db.session.get(User, user_id)
    # Check if we get a user back or None
    if user is not None:
        return user_output_schema.jsonify(user)
    return {"error": f"User with ID {user_id} does not exist"}, 404 # Not Found

@app.route('/users', methods=["POST"])
@limiter.limit("100 per day")
def create_user():
    if not request.is_json:
        return jsonify({"error": "Request body must be application/json"}), 400
    try:
        data = request.json
        # Validate and deserialize input
        user_data = user_input_schema.load(data)
        # Check if the user already exists
        query = db.select(User).where((User.username == user_data['username']) | (User.email == user_data['email']))
        check_users = db.session.scalars(query).all()

        if check_users:
            return jsonify({"error": "User with that username and/or email already exists"}), 400

        # Create new user
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            email=user_data['email'],
            password=generate_password_hash(user_data['password']),
            role_id=user_data['role_id']  # Use the role_id from the user_data
        )

        db.session.add(new_user)
        db.session.commit()

        return user_output_schema.jsonify(new_user), 201

    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except SQLAlchemyError as err:
        return jsonify({"error": "An error occurred while creating the user: " + str(err)}), 500


# Admin-only Endpoint
@app.route('/admin')
@token_auth.login_required(role='admin')
def admins_only():
    return "Hello {} {} (username: {}), you are an admin!".format(token_auth.current_user().first_name, token_auth.current_user().last_name, token_auth.current_user().username)

# Update a user by ID (Admin Only)
@app.route('/users/<int:user_id>', methods=["PUT"])
@token_auth.login_required(role='admin')
@limiter.limit("100 per day")
def update_user(user_id):
    # Check if the request has a JSON body
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400
    try:
        # Get the request JSON body
        data = request.json
        # Load the data into the schema, ignoring missing fields for partial updates
        user_data = user_input_schema.load(data, partial=True)
        
        # Fetch the user from the database
        user = db.session.get(User, user_id)
        if user is None:
            return {"error": f"User with ID {user_id} does not exist"}, 404
        
        # Update the user fields
        for key, value in user_data.items():
            if key == 'password':
                value = generate_password_hash(value)
            if key == 'role' and isinstance(value, Role):
                # Fetch the actual Role object from the database
                role = db.session.execute(db.select(Role).where(Role.role_name == value.role_name)).scalar()
                if not role:
                    return jsonify({"error": "Role not found"}), 400
                user.role = role
            else:
                setattr(user, key, value)
        
        # Commit the changes
        db.session.commit()
        
        return user_output_schema.jsonify(user)
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400

# Delete a user by ID (Admin Only):
@app.route('/users/<int:user_id>', methods=["DELETE"])
@token_auth.login_required(role='admin')
@limiter.limit("100 per day")
def delete_user(user_id):
    # Fetch the user from the database
    user = db.session.get(User, user_id)
    if user is None:
        return {"error": f"User with ID {user_id} does not exist"}, 404
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    
    return {"message": f"User with ID {user_id} has been deleted"}, 200

# ==== Posts Endpoints ====

# Get all posts
@app.route('/posts', methods=["GET"])
@token_auth.login_required
@limiter.limit("100 per day")
@cache.cached(timeout=60)
def get_all_posts():
    # app.logger.info("Entering get_all_posts")
    # sys.stdout.flush()
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    search = args.get('search', '')
    # query = db.select(Post)
    query = db.select(Post).where(Post.title.like(f'%{search}%')).limit(per_page).offset((page-1)*per_page)
    posts = db.session.scalars(query).all()
    # app.logger.info(f"Fetched posts: {posts}")
    # sys.stdout.flush()
    return posts_schema.jsonify(posts)   

# Get a single post by ID
@app.route('/posts/<int:post_id>', methods=["GET"])
@token_auth.login_required
@limiter.limit("100 per day")
@cache.cached(timeout=60)
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
@limiter.limit("100 per day")
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
    
# Update a post by ID
@app.route('/posts/<int:post_id>', methods=["PUT"])
@token_auth.login_required
@limiter.limit("100 per day")
def update_post(post_id):
    # Check if the request has a JSON body
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400
    try:
        # Get the request JSON body
        data = request.json
        # Load the data into the schema, ignoring missing fields for partial updates
        post_data = post_schema.load(data, partial=True)
        
        # Fetch the post from the database
        post = db.session.get(Post, post_id)
        if post is None:
            return {"error": f"Post with ID {post_id} does not exist"}, 404

        # Ensure the user updating the post is the author
        current_user = token_auth.current_user()
        if post.user_id != current_user.user_id:
            return {"error": "You do not have permission to update this post"}, 403
        
        # Update the post fields
        for key, value in post_data.items():
            setattr(post, key, value)
        
        # Commit the changes
        db.session.commit()
        
        return post_schema.jsonify(post)
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400

# Delete a post by ID
@app.route('/posts/<int:post_id>', methods=["DELETE"])
@token_auth.login_required
@limiter.limit("100 per day")
def delete_post(post_id):
    # Fetch the post from the database
    post = db.session.get(Post, post_id)
    if post is None:
        return {"error": f"Post with ID {post_id} does not exist"}, 404
    
    # Ensure the user deleting the post is the author
    current_user = token_auth.current_user()
    if post.user_id != current_user.user_id:
        return {"error": "You do not have permission to delete this post"}, 403
    
    # Delete the post
    db.session.delete(post)
    db.session.commit()
    
    return {"message": f"Post with ID {post_id} has been deleted"}, 200

# ==== Comments Endpoints ====

# Get all comments
@app.route('/comments', methods=['GET'])
@token_auth.login_required
@limiter.limit("100 per day")
@cache.cached(timeout=60)
def get_all_comments():
    # app.logger.info("Entering get_all_comments")
    # sys.stdout.flush()
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    # query = db.select(Post)
    query = db.select(Comment).limit(per_page).offset((page-1)*per_page)
    # query = db.select(Comment) # select the Comment model
    comments = db.session.execute(query).scalars().all()
    # app.logger.info(f"Fetched comments: {comments}")
    # sys.stdout.flush()
    return comments_schema.jsonify(comments)

# Get a single comment by ID
@app.route('/comments/<int:comment_id>', methods=["GET"])
@token_auth.login_required
@limiter.limit("100 per day")
@cache.cached(timeout=60)
def get_single_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if comment is not None:
        return comment_schema.jsonify(comment)
    return {"error": f"Comment with ID {comment_id} does not exist"}, 404

# Create a new comment
@app.route('/comments', methods=["POST"])
@token_auth.login_required
@limiter.limit("100 per day")
def create_comment():
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400
    try:
        data = request.json
        comment_data = comment_schema.load(data)

        current_user = token_auth.current_user()
        new_comment = Comment(
            content=comment_data['content'],
            user_id=current_user.user_id,
            post_id=comment_data['post_id']
        )
        db.session.add(new_comment)
        db.session.commit()
        
        return comment_schema.jsonify(new_comment), 201
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400

# Update a comment
@app.route('/comments/<int:comment_id>', methods=["PUT"])
@token_auth.login_required
@limiter.limit("100 per day")
def update_comment(comment_id):
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400
    try:
        data = request.json
        comment_data = comment_schema.load(data)

        comment = db.session.get(Comment, comment_id)
        if comment is None:
            return {"error": f"Comment with ID {comment_id} does not exist"}, 404

        current_user = token_auth.current_user()
        if comment.user_id != current_user.user_id:
            return {"error": "Unauthorized to update this comment"}, 403

        comment.content = comment_data['content']
        db.session.commit()

        return comment_schema.jsonify(comment)
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400

# Delete a comment by ID (Admin Only)
@app.route('/comments/<int:comment_id>', methods=["DELETE"])
@token_auth.login_required(role='admin')
@limiter.limit("100 per day")
def delete_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if comment is None:
        return {"error": f"Comment with ID {comment_id} does not exist"}, 404

    # The @token_auth.login_required(role='admin') decorator ensures that only admins can access this route.
    # No need for further role checks inside the function:

    # current_user = token_auth.current_user()
    # if comment.user_id != current_user.user_id:
    #     return {"error": "Unauthorized to delete this comment"}, 403

    db.session.delete(comment)
    db.session.commit()

    return {"message": f"Comment with ID {comment_id} has been deleted"}, 200

# List all comments for a specific post
@app.route('/posts/<int:post_id>/comments', methods=["GET"])
@token_auth.login_required
@limiter.limit("100 per day")
@cache.cached(timeout=60)
def list_comments(post_id):
    query = db.select(Comment).where(Comment.post_id == post_id)
    comments = db.session.scalars(query).all()
    return comments_schema.jsonify(comments)