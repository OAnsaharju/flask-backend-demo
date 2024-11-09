""" Tests for /user endpoints """

from constants import TEST_USER_EMAIL, TEST_USER_2_EMAIL, TEST_USER_PASSWORD


def test_register_user(client):
    """Test that a new user can register"""

    payload = {"email": TEST_USER_2_EMAIL, "password": TEST_USER_PASSWORD}
    response = client.post("/register", json=payload)

    assert response.status_code == 201

    response_data = response.get_json()
    expected_data = {"message": "User registered successfully"}
    assert response_data == expected_data


def test_login_user(client):
    """Test that a registered user can log in"""

    payload = {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
    response = client.post("/login", json=payload)

    assert response.status_code == 200

    response_data = response.get_json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
