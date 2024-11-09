from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.group_model import Group
from models.person_model import Person
from models.schemas.group_model_schema import GroupModelSchema
from routes.schemas.group_route_schema import (
    GroupPayloadSchema,
    GroupResponsePayloadSchema,
)

group_bp = Blueprint("group_bp", __name__)

# Initialize schemas
group_schema = GroupModelSchema()
groups_schema = GroupModelSchema(many=True)
group_response_payload_schema = GroupResponsePayloadSchema()
groups_response_payload_schema = GroupResponsePayloadSchema(many=True)
group_payload_schema = GroupPayloadSchema()


# Create a new group
@group_bp.route("/groups", methods=["POST"])
@jwt_required()
def create_group():
    data = request.json
    errors = group_payload_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user_id = get_jwt_identity()

    # Validate persons if they are associated with the user
    if "persons" in data:
        person_ids = data.get("persons")
        persons = Person.query.filter(
            Person.id.in_(person_ids), Person.user_id == user_id
        ).all()
        if len(persons) != len(person_ids):
            return (
                jsonify(
                    {
                        "error": "One or more persons do not belong to the user or don't exist"
                    }
                ),
                400,
            )
        data["persons"] = persons

    data["user_id"] = user_id
    new_group = group_schema.load(data)

    db.session.add(new_group)
    db.session.commit()

    return group_schema.jsonify(new_group), 201


@group_bp.route("/groups", methods=["GET"])
@jwt_required()
def get_groups():
    user_id = get_jwt_identity()
    groups = Group.query.filter_by(user_id=user_id).all()
    return groups_response_payload_schema.jsonify(groups), 200


@group_bp.route("/groups/<int:group_id>", methods=["GET"])
@jwt_required()
def get_group(group_id):
    user_id = get_jwt_identity()
    group = Group.query.filter_by(user_id=user_id, id=group_id).first_or_404()

    return group_response_payload_schema.jsonify(group), 200


@group_bp.route("/groups/<int:group_id>", methods=["PUT"])
@jwt_required()
def update_group(group_id):
    user_id = get_jwt_identity()
    group = Group.query.filter_by(user_id=user_id, id=group_id).first_or_404()

    data = request.json
    errors = group_payload_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    # Validate persons if they are associated with the user
    if "persons" in data:
        person_ids = data.get("persons")
        persons = Person.query.filter(
            Person.id.in_(person_ids), Person.user_id == user_id
        ).all()
        if len(persons) != len(person_ids):
            return (
                jsonify(
                    {
                        "error": "One or more persons do not belong to the user or don't exist"
                    }
                ),
                400,
            )
        group.persons = persons

    if "name" in data:
        group.name = data["name"]
    if "description" in data:
        group.description = data["description"]

    db.session.commit()

    return group_payload_schema.jsonify(group), 200


# Delete a group
@group_bp.route("/groups/<int:group_id>", methods=["DELETE"])
@jwt_required()
def delete_group(group_id):
    user_id = get_jwt_identity()
    group = Group.query.filter_by(user_id=user_id, id=group_id).first_or_404()

    db.session.delete(group)
    db.session.commit()

    return jsonify({"message": "Group deleted"}), 200
