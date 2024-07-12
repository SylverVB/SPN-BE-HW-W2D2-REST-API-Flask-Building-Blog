from app.database import db
from sqlalchemy.orm import Mapped, mapped_column

class Comment(db.Model):
    comment_id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(db.Text, nullable=False)
    post_id: Mapped[int] = mapped_column(db.ForeignKey('post.post_id'), nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.user_id'), nullable=False)
    post = db.relationship('Post', back_populates='comments')
    user = db.relationship('User', back_populates='comments')