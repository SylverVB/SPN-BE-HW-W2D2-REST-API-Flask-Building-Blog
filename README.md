# Advanced Blog API

## Overview

The Advanced Blog API is a fully-featured blogging platform built with Flask. It supports CRUD operations for users, posts, and comments. The API uses JWT-based authentication for secure access to endpoints, and it includes comprehensive documentation with Swagger. Unit tests ensure the reliability and stability of the API.

## Table of Contents

- [Advanced Blog API](#advanced-blog-api)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
  - [API Documentation](#api-documentation)
  - [API Endpoints](#api-endpoints)
    - [Token](#token)
    - [Users](#users)
    - [Posts](#posts)
    - [Comments](#comments)
  - [Project Structure](#project-structure)
    - [app/\_\_init.py](#app__initpy)
    - [app/auth.py](#appauthpy)
    - [app/database.py](#appdatabasepy)
    - [app/models/](#appmodels)
    - [app/routes.py](#approutespy)
    - [app/schemas/](#appschemas)
    - [app/utils/](#apputils)
    - [tests/](#tests)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contributors License Agreement (CLA)](#contributors-license-agreement-cla)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SylverVB/SPN-BE-HW-W2D2-REST-API-Flask-Building-Blog.git
   cd SPN-BE-HW-W2D2-REST-API-Flask-Building-Blog
   ```

2. **Create a virtual environment:**

   - **On macOS and Linux:**

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - **On Windows:**

     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the root of your project with the following content:

```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

Replace `your_database_url` with the URL of your database and `your_secret_key` with a secret key for signing JWT tokens.

## Running the Application

1. **Initialize the database:**

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

2. **Run the Flask application:**

   ```bash
   flask run
   ```

The application will be available at `http://127.0.0.1:5000`.

## Running Tests

To run the unit tests for the application, use the following command:

```bash
pytest
```

Or

```bash
python -m unittest discover -v
```

This will execute all tests located in the `tests` directory and provide a summary of the results.

## API Documentation

The API documentation is available via Swagger. After starting the application, navigate to `http://127.0.0.1:5000/api/docs/` to view the interactive API documentation.

## API Endpoints

### Token

- **Get a token**: `POST /token`

### Users

- **Get all users**: `GET /users`
- **Get a single user by ID**: `GET /users/{user_id}`
- **Create a new user**: `POST /users`
- **Update a user by ID**: `PUT /users/{user_id}`
- **Delete a user by ID**: `DELETE /users/{user_id}`

### Posts

- **Get all posts**: `GET /posts`
- **Get a single post by ID**: `GET /posts/{post_id}`
- **Get comments for a post**: `GET /posts/{post_id}/comments`
- **Create a new post**: `POST /posts`
- **Update a post by ID**: `PUT /posts/{post_id}`
- **Delete a post by ID**: `DELETE /posts/{post_id}`

### Comments

- **Get all comments**: `GET /comments`
- **Get a single comment by ID**: `GET /comments/{comment_id}`
- **Create a new comment**: `POST /comments`
- **Update a comment by ID**: `PUT /comments/{comment_id}`
- **Delete a comment by ID**: `DELETE /comments/{comment_id}`

## Project Structure

```bash
flask-blog-api/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── caching.py
│   ├── limiter.py
│   ├── routes.py
│   ├── swagger_docs.py
│   ├── database.py
│   ├── assignments/
│   │   ├── first_commit_rest_api_design_patterns.py
│   │   ├── second_third_commits_api_security.py
│   │   ├── fourth_commit_advanced_blog_api_mini_project.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── post.py
│   │   ├── user.py
│   │   ├── comment.py
│   │   ├── role.py
│   ├── static/
│   │   ├── swagger.yaml
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── postSchema.py
│   │   ├── userSchema.py
│   │   ├── commentSchema.py
│   ├── utils/
│   │   ├── util.py
├── migrations/
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
├── venv/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
```

### app/__init.py

Initializes the Flask application, configures the SQLAlchemy database, and imports the routes and models.

### app/auth.py

Handles JWT token authentication using Flask-HTTPAuth.

### app/database.py

Sets up SQLAlchemy and Flask-Migrate for database operations and migrations.

### app/models/

Contains the SQLAlchemy models for `User`, `Post`, and `Comment`.

### app/routes.py

Defines the routes for the API, including user, post, and comment endpoints, as well as the token generation endpoint.

### app/schemas/

Contains Marshmallow schemas for serializing and deserializing `User`, `Post`, and `Comment` objects.

### app/utils/

Includes utility functions for encoding and decoding JWT tokens.

### tests/

Contains unit tests for the application, ensuring the correctness of authentication, user, post, and comment functionalities.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This application is the property of Victor Bondaruk. As the owner, [Victor Bondaruk](https://github.com/SylverVB) retains all rights to the application.

## Contributors License Agreement (CLA)
By making a contribution to this project, you agree to the following terms and conditions for your contributions:

1. You grant the owner, Victor Bondaruk, a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable license to use, distribute, and modify your contributions as part of this project.
2. You represent that you are legally entitled to grant the above license.
3. You agree to promptly notify the owner of any facts or circumstances of which you become aware that would make these representations inaccurate in any respect.