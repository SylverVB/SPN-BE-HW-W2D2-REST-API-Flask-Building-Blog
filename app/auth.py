from flask_httpauth import HTTPTokenAuth
from app.utils.util import decode_token
from app.models import User
from app.database import db


# Create an instance of the HTTPTokenAuth class
token_auth = HTTPTokenAuth(scheme='Bearer')


@token_auth.verify_token
def verify(token):
    # Decode the token to get the user id
    user_id = decode_token(token)
    if user_id is not None:
        # Get the user with that ID
        return db.session.get(User, user_id)
    else:
        return None


@token_auth.error_handler
def handle_error(status_code):
    return {"error": "Invalid token. Please try again"}, status_code