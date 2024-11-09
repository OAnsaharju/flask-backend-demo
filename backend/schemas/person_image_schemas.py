from flask_marshmallow import Marshmallow
from marshmallow import fields
from models.person_image_model import (
    PersonImage,
)


ma = Marshmallow()


class PersonImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PersonImage
        include_fk = True
        load_instance = True

    url = fields.String(required=True)
    person_id = fields.Integer(dump_only=True)


class PersonImagePayloadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PersonImage
        load_instance = True
        exclude = (
            "person_id",
            "s3_object_name",
        )

    url = fields.String(required=True)
