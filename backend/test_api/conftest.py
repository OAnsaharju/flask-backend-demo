""" Testing fixtures """

import pytest
from models import db
from routes.util_routes import generate as generate_test_data
from constants import TEST_USER_EMAIL, TEST_USER_PASSWORD
from app import app


@pytest.fixture(scope="session", autouse=True)
def clean():
    """Fixture that makes sure db is clean before a pytest session"""
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client():
    """API test fixture"""

    with app.test_client() as test_client:
        # set up
        app.config.update(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        with app.app_context():
            db.create_all()
            generate_test_data()

        # run test
        yield test_client

        # tear down
        db.drop_all()


@pytest.fixture()
def authorized_client(client):
    """Login fixture"""

    payload = {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
    response = client.post("/login", json=payload)

    assert response.status_code == 200

    token = response.get_json()["access_token"]
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    return client
