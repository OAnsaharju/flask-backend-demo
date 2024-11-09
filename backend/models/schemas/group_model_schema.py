from flask_marshmallow import Marshmallow
from marshmallow import fields
from models.group_model import (
    Group,
)

from models.schemas.person_model_schema import PersonModelSchema

ma = Marshmallow()


class GroupModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Group
        include_relationships = True
        load_instance = True

    name = fields.String(required=True, validate=lambda n: len(n) > 0)
    description = fields.String(allow_none=True)
    persons = fields.List(fields.Nested(PersonModelSchema), required=False)
