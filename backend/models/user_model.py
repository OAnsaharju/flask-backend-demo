from . import db, bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    # Relationship to person
    persons = db.relationship(
        "Person", back_populates="user", cascade="all, delete-orphan"
    )
    # Relationship for group
    groups = db.relationship(
        "Group", back_populates="user", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "groups": [group.to_dict() for group in self.groups],
        }

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
