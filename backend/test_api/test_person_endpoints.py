from test_data import (
    expected_get_persons_response,
    expected_create_new_person_response,
    expected_get_single_person_response,
)

""" Tests for /person endpoints """


def test_get_persons(authorized_client):
    """Test getting all (10) persons"""

    response = authorized_client.get("/persons")

    assert response.status_code == 200
    response_data = response.get_json()
    assert len(response_data) == 10
    assert response_data == expected_get_persons_response


def test_add_new_person(authorized_client):
    """Test creating a new person"""
    payload = {
        "first_name": "Teppo",
        "last_name": "Tulppu",
        "nick_names": ["TT", "T-boy"],
    }
    response = authorized_client.post("/persons", json=payload)
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data == expected_create_new_person_response


def test_get_single_person(authorized_client):
    """Test getting a single person by id"""
    response = authorized_client.get("/persons/1")
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data == expected_get_single_person_response


def test_delete_single_person(authorized_client):
    """Test deleting a single person by id"""
    response = authorized_client.delete("/persons/1")
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data == {"message": "Person deleted"}
