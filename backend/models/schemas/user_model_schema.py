from flask_marshmallow import Marshmallow
from marshmallow import fields
from models.user_model import User

ma = Marshmallow()


class UserModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        exclude = ("password_hash",)  # Exclude sensitive data

    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        load_only=True,  # Prevent password from being serialized in responses
    )
