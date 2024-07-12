from flask_httpauth import HTTPTokenAuth
from app.utils.util import decode_token
from app.models import User
from app.database import db
# import logging

# # Configure logger
# logger = logging.getLogger(__name__)

# Create an instance of the HTTPTokenAuth class
token_auth = HTTPTokenAuth(scheme='Bearer')


@token_auth.verify_token
def verify(token):
    # Decode the token to get the user id
    user_id = decode_token(token)
    # logger.info(f"Decoded user ID: {user_id}")
    if user_id is not None:
        user = db.session.get(User, user_id)
        if user:
            # logger.info(f"User found: {user}")
            return user
        else:
            # logger.info(f"No user found with user_id: {user_id}")
            return None
    else:
        # logger.info("Invalid token or token decoding failed")
        return None
    

@token_auth.error_handler
def handle_error(status_code):
    # logger.info(f"Handling error with status code: {status_code}")
    if status_code == 401:
        return {"error": "Invalid token. Please try again"}, 401
    elif status_code == 403:
        return {"error": "Unauthorized to access this resource"}, 403
    else:
        return {"error": "An unknown error occurred"}, status_code


@token_auth.get_user_roles
def get_roles(user):
    return [user.role.role_name]