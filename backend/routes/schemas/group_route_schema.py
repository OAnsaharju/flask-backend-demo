from flask_marshmallow import Marshmallow, Schema
from marshmallow import fields, pre_dump
from models.group_model import (
    Group,
)

ma = Marshmallow()


class GroupPayloadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Group
        include_relationships = True
        load_instance = True
        exclude = ("user_id",)

    name = fields.String(required=True, validate=lambda n: len(n) > 0)
    description = fields.String(allow_none=True)


class GroupResponsePayloadSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True, validate=lambda n: len(n) > 0)
    description = fields.String(allow_none=True)
    persons = fields.List(fields.Integer(), required=False)

    @pre_dump(pass_many=True)
    def flatten_person(self, data, many, **kwargs):
        if many:
            mapped_data = [
                {**group.__dict__, "persons": [person.id for person in group.persons]}
                for group in data
            ]
        else:
            mapped_data = {
                **data.__dict__,
                "persons": [person.id for person in data.persons],
            }
        return mapped_data
