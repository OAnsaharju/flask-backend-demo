import uuid
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, app, redirect, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from utils.blurhash import generate_blurhash
from utils.s3 import create_presigned_url, delete_from_s3, upload_to_s3
from botocore.exceptions import BotoCoreError, ClientError
from models import db
from models.person_model import Person
from models.person_image_model import PersonImage
from models.schemas.group_model_schema import GroupModelSchema
from routes.schemas.group_route_schema import GroupPayloadSchema
from models.schemas.user_model_schema import UserModelSchema
from schemas.person_image_schemas import PersonImagePayloadSchema, PersonImageSchema
from models.schemas.person_model_schema import PersonModelSchema
from routes.schemas.person_route_schema import PersonPayloadSchema

from faker import Faker

fake = Faker()

person_bp = Blueprint("person_bp", __name__)

user_schema = UserModelSchema()
person_schema = PersonModelSchema()
person_payload_schema = PersonPayloadSchema()

persons_schema = PersonModelSchema(many=True)
person_image_schema = PersonImageSchema()
person_images_schema = PersonImageSchema(many=True)
person_image_payload_schema = PersonImagePayloadSchema()
person_images_payload_schema = PersonImagePayloadSchema(many=True)
group_schema = GroupModelSchema()
group_payload_schema = GroupPayloadSchema()


def validate_ownership(person_id):
    user_id = get_jwt_identity()
    person = Person.query.filter_by(id=person_id, user_id=user_id).first_or_404()
    return person, user_id


@person_bp.route("/persons", methods=["POST"])
@jwt_required()
def create_person():
    data = request.json

    errors = person_payload_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user_id = get_jwt_identity()
    data["user_id"] = user_id

    new_person = person_schema.load(data)

    db.session.add(new_person)
    db.session.commit()

    return person_schema.jsonify(new_person), 201


@person_bp.route("/persons", methods=["GET"])
@jwt_required()
def get_persons():
    user_id = get_jwt_identity()
    persons = Person.query.filter_by(user_id=user_id).all()

    modified_persons = []
    for person in persons:

        default_image = PersonImage.query.filter_by(
            person_id=person.id, id=person.default_image_id
        ).first()

        person_data = person_schema.dump(person)
        person_data["default_image"] = (
            {
                "id": default_image.id,
                "url": default_image.url,
                "blurhash": default_image.blurhash,
            }
            if default_image
            else None
        )

        person_data.pop("user_id", None)
        person_data.pop("user", None)

        modified_persons.append(person_data)

    return jsonify(modified_persons)


@person_bp.route("/persons/<int:person_id>", methods=["GET"])
@jwt_required()
def get_person(person_id):
    person, _ = validate_ownership(person_id)

    default_image = PersonImage.query.filter_by(
        person_id=person.id, id=person.default_image_id
    ).first()

    person_data = person_schema.dump(person)
    person_data["default_image"] = (
        {
            "id": default_image.id,
            "url": default_image.url,
            "blurhash": default_image.blurhash,
        }
        if default_image
        else None
    )

    return jsonify(person_data), 200


@person_bp.route("/persons/<int:person_id>", methods=["PUT"])
@jwt_required()
def update_person(person_id):
    person, _ = validate_ownership(person_id)

    data = request.json
    errors = person_payload_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    person = person_schema.load(data, instance=person, partial=True)
    db.session.commit()

    return person_schema.jsonify(person), 200


@person_bp.route("/persons/<int:person_id>", methods=["DELETE"])
@jwt_required()
def delete_person(person_id):
    person, _ = validate_ownership(person_id)

    db.session.delete(person)
    db.session.commit()

    return jsonify({"message": "Person deleted"}), 200


@person_bp.route("/persons/<int:person_id>/images", methods=["POST"])
@jwt_required()
async def create_person_image(person_id):
    try:
        _, user_id = validate_ownership(person_id)

        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No image provided"}), 400

        file_data = file.read()
        if not file_data:
            return jsonify({"error": "File is empty"}), 400
        file_id = uuid.uuid4()
        s3_object_name = f"{user_id}/image_{person_id}_{file_id}.jpeg"

        try:
            await upload_to_s3(file_data, s3_object_name)
        except (BotoCoreError, ClientError) as s3_error:
            app.logger.error(f"S3 upload failed: {s3_error}")
            return jsonify({"error": "Failed to upload image to S3 storage"}), 500

        blurhash_str = generate_blurhash(file_data)

        new_image_data = {
            "url": f"persons/{person_id}/images/{file_id}/asset",
            "s3_object_name": s3_object_name,
            "blurhash": blurhash_str,
        }

        new_image = person_image_schema.load(new_image_data)

        new_image.person_id = person_id
        db.session.add(new_image)
        db.session.commit()

        return person_image_payload_schema.jsonify(new_image), 201

    except HTTPException as http_error:

        app.logger.error(f"HTTP error during image creation: {http_error}")
        return jsonify({"error": str(http_error)}), http_error.code

    except SQLAlchemyError as db_error:
        db.session.rollback()
        app.logger.error(f"Database error during image creation: {db_error}")
        return jsonify({"error": "An error occurred while saving the image"}), 500

    except Exception as e:
        app.logger.error(f"Unexpected error during image creation: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@person_bp.route("/persons/<int:person_id>/images/<int:image_id>", methods=["DELETE"])
@jwt_required()
async def remove_person_image(person_id, image_id):
    try:

        validate_ownership(person_id)

        person_image = PersonImage.query.filter_by(
            person_id=person_id, id=image_id
        ).first_or_404()

        if person_image.s3_object_name is not None:
            try:
                await delete_from_s3(person_image.s3_object_name)
            except (BotoCoreError, ClientError) as s3_error:

                app.logger.error(f"S3 deletion failed: {s3_error}")
                return (
                    jsonify({"error": "Failed to delete image from S3 storage."}),
                    500,
                )

        db.session.delete(person_image)
        db.session.commit()

        return jsonify({"message": "PersonImage deleted"}), 200

    except HTTPException as http_error:

        app.logger.error(f"HTTP error during deletion: {http_error}")
        return jsonify({"error": str(http_error)}), http_error.code

    except SQLAlchemyError as db_error:

        db.session.rollback()
        app.logger.error(f"Database error during image deletion: {db_error}")
        return (
            jsonify(
                {"error": "An error occurred while deleting the image in the database."}
            ),
            500,
        )

    except Exception as e:
        app.logger.error(f"Unexpected error during image deletion: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500


@person_bp.route(
    "/persons/<int:person_id>/images/<string:file_id>/asset", methods=["GET"]
)
@jwt_required()
async def get_person_image_asset(person_id, file_id):
    validate_ownership(person_id)

    image = (
        PersonImage.query.filter_by(person_id=person_id)
        .filter(PersonImage.s3_object_name.contains(file_id))
        .first_or_404()
    )

    presigned_url = await create_presigned_url(image.s3_object_name)

    return redirect(presigned_url, code=302)


@person_bp.route("/persons/<int:person_id>/images", methods=["GET"])
@jwt_required()
def get_person_images(person_id):
    validate_ownership(person_id)

    images = PersonImage.query.filter_by(person_id=person_id).all()

    return person_images_payload_schema.jsonify(images), 200
