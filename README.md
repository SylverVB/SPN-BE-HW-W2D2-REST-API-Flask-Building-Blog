# Flask Blog API

## Overview

This project is a Blog API built using Flask, incorporating Flask-SQLAlchemy for ORM and Flask-Migrate for database migrations. The API supports CRUD operations for users and posts, and includes JWT-based authentication for secure access to the endpoints.

## Table of Contents

1. [Installation](#installation)
2. [Environment Variables](#environment-variables)
3. [Running the Application](#running-the-application)
4. [API Endpoints](#api-endpoints)
5. [Authentication](#authentication)
6. [Project Structure](#project-structure)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SylverVB/SPN-BE-HW-W2D2-REST-API-Flask-Building-Blog.git
   cd SPN-BE-HW-W2D2-REST-API-Flask-Building-Blog
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
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

## API Endpoints

### Users

- **Get all users**: `GET /users`
- **Get a single user by ID**: `GET /users/<int:user_id>`
- **Create a new user**: `POST /users`

### Posts

- **Get all posts**: `GET /posts`
- **Get a single post by ID**: `GET /posts/<int:post_id>`
- **Create a new post**: `POST /posts` (Requires JWT Token)

### Token

- **Get a token**: `POST /token`

## Authentication

The API uses JWT tokens for authentication. To get a token, you need to call the `/token` endpoint with a valid username and password. The token should be included in the `Authorization` header as a Bearer token for endpoints that require authentication.

### Example

To create a new post, use the following cURL command:

```bash
curl -X POST http://127.0.0.1:5000/posts \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your_jwt_token" \
-d '{
    "title": "OOP in Python",
    "body": "Object-oriented programming (OOP) is a method of structuring a program by bundling related properties and behaviors into individual objects. In this post, you’ll learn the basics of object-oriented programming in Python."
}'
```

Replace `your_jwt_token` with the token you obtained from the `/token` endpoint.

## Project Structure

```bash
flask-blog-api/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── post.py
│   │   ├── user.py
│   ├── routes.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── postSchema.py
│   │   ├── userSchema.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── util.py
├── migrations/
├── venv/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
```

### app/__init__.py

Initializes the Flask application, configures the SQLAlchemy database, and imports the routes and models.

### app/auth.py

Handles JWT token authentication using Flask-HTTPAuth.

### app/database.py

Sets up SQLAlchemy and Flask-Migrate for database operations and migrations.

### app/models/

Contains the SQLAlchemy models for `User` and `Post`.

### app/routes.py

Defines the routes for the API, including user and post endpoints, as well as the token generation endpoint.

### app/schemas/

Contains Marshmallow schemas for serializing and deserializing `User` and `Post` objects.

### app/utils/

Includes utility functions for encoding and decoding JWT tokens.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This application is the property of Victor Bondaruk. As the owner, [Victor Bondaruk](https://github.com/SylverVB) retains all rights to the application.

## Contributors License Agreement (CLA)
By making a contribution to this project, you agree to the following terms and conditions for your contributions:

1. You grant the owner, Victor Bondaruk, a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable license to use, distribute, and modify your contributions as part of this project.
2. You represent that you are legally entitled to grant the above license.
3. You agree to promptly notify the owner of any facts or circumstances of which you become aware that would make these representations inaccurate in any respect.