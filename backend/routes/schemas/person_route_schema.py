from flask_marshmallow import Marshmallow
from models.person_model import Person

ma = Marshmallow()


class PersonPayloadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Person
        include_relationships = True
        load_instance = True
        exclude = ("user_id",)
