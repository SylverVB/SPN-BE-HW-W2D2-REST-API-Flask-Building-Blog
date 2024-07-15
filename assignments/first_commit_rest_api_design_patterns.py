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