from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .associations import group_person_association


class Person(db.Model):
    __tablename__ = "person"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    first_name = db.Column(db.String(40), nullable=True)
    last_name = db.Column(db.String(40), nullable=True)
    nick_names = db.Column(db.JSON(db.String), nullable=False)
    # todo: consider changing to relationship?
    default_image_id = db.Column(db.Integer, nullable=True)

    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="persons")

    images = relationship(
        "PersonImage", back_populates="person", cascade="all, delete-orphan"
    )

    # Many-to-Many with Groups. Person can belong to multiple groups
    groups = db.relationship(
        "Group", secondary=group_person_association, back_populates="persons"
    )
