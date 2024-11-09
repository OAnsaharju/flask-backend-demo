from flask import Blueprint, jsonify
from models import db
from models.group_model import Group
from models.person_model import Person
from models.person_image_model import PersonImage
from models.user_model import User

from models.schemas.person_model_schema import PersonModelSchema
from schemas.person_image_schemas import PersonImageSchema

from faker import Faker

util_bp = Blueprint("util_bp", __name__)
fake = Faker()
Faker.seed(0)

person_schema = PersonModelSchema()
person_image_schema = PersonImageSchema()


@util_bp.route("/generate", methods=["GET"])
def generate():

    # Clear existing data
    PersonImage.query.delete()
    Person.query.delete()
    Group.query.delete()
    User.query.delete()

    user = User(email="test@test.com")
    user.set_password("Testtest1+")
    db.session.add(user)
    db.session.commit()
    user_temp = db.session.query(User).first()
    print(user_temp.id)

    persons_list_1 = []
    persons_list_2 = []

    for x in range(10):
        new_person = person_schema.load(
            {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "nick_names": [
                    fake.first_name(),
                    fake.first_name(),
                ],
                "user_id": user_temp.id,
            }
        )
        db.session.add(new_person)
        db.session.commit()

        if len(persons_list_1) < 5:
            persons_list_1.append(new_person)
        else:
            persons_list_2.append(new_person)

        for x in range(10):
            new_person_image = person_image_schema.load(
                {
                    "url": f"https://picsum.photos/seed/prosopagnosia-{new_person.id}-{x}/1024",
                }
            )
            new_person_image.person_id = new_person.id
            db.session.add(new_person_image)
            db.session.commit()
            new_person.default_image_id = new_person_image.id
            db.session.commit()

    new_group = Group(
        name="Mock Group",
        description="This is a mock group generated for testing purposes.",
        user_id=user_temp.id,
        persons=persons_list_1,
    )

    db.session.add(new_group)

    another_group = Group(
        name="Mock Group 2",
        description="This is another mock group generated for testing purposes.",
        user_id=user_temp.id,
        persons=persons_list_2,
    )

    db.session.add(another_group)

    db.session.commit()

    return jsonify({"message": "mock data generated"}), 200
