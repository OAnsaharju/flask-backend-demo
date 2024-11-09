from marshmallow import Schema, fields, ValidationError


def validate_password_strength(value):
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(char.islower() for char in value):
        raise ValidationError("Password must contain a lowercase letter.")
    if not any(char.isupper() for char in value):
        raise ValidationError("Password must contain an uppercase letter.")
    if not any(char.isdigit() for char in value):
        raise ValidationError("Password must contain a digit.")
    if not any(char in "@#$%^&+=" for char in value):
        raise ValidationError("Password must contain a special character.")


class UserPayloadSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(
        required=True, validate=validate_password_strength, load_only=True
    )
