from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .associations import group_person_association


class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    # Many-to-One with User. Group is created by a User.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="groups")

    # Many-to-Many with Person. A group can have many persons, and persons can belong to many groups.
    persons = db.relationship(
        "Person", secondary=group_person_association, back_populates="groups"
    )
