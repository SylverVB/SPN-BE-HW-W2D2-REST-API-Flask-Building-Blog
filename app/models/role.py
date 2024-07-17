from app.database import db
from sqlalchemy.orm import Mapped, mapped_column

class Role(db.Model):
    role_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    users = db.relationship('User', back_populates='role')

    def __str__(self):
        return f"{self.role_name}"