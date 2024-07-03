from app.database import db
from sqlalchemy.orm import Mapped, mapped_column

class Post(db.Model):
    post_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    body: Mapped[str] = mapped_column(db.Text)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', back_populates='posts')