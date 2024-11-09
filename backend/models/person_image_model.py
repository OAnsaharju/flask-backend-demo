from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class PersonImage(db.Model):
    __tablename__ = "person_image"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    person_id = db.Column(db.Integer, ForeignKey("person.id"), nullable=False)
    url = db.Column(db.String(500), unique=False, nullable=False)
    s3_object_name = db.Column(db.String(500), unique=True, nullable=True)
    blurhash = db.Column(db.String(500), unique=False, nullable=True)

    person = db.relationship("Person", back_populates="images")
