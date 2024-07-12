from app.database import db
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    username: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(db.ForeignKey('role.role_id'), default=2)
    role = db.relationship('Role', back_populates='users')
    posts = db.relationship('Post', order_by='Post.post_id', back_populates='user')
    # With cascade='all, delete-orphan', deleting a user would delete all associated comments,
    # removing a comment from a User's comments collection would delete it from the database:
    comments = db.relationship('Comment', order_by='Comment.comment_id', back_populates='user', cascade='all, delete-orphan')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User {self.user_id}|{self.username}>"