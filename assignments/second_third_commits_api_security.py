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