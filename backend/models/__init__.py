from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

# Import models so that they get registered with SQLAlchemy
from .user_model import User
from .person_model import Person
from .person_image_model import PersonImage
from .group_model import Group
from .associations import group_person_association
