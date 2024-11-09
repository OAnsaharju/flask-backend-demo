from flask_marshmallow import Marshmallow
from marshmallow import fields
from models.person_model import Person

ma = Marshmallow()


class PersonModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Person
        include_relationships = True
        load_instance = True
