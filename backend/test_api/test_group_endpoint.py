from test_data import (
    expected_groups_response,
    expected_single_group_response,
    expected_create_group_response,
    expected_update_group_response,
    expected_delete_group_response,
)

"""Tests for group endpoints"""


def test_get_all_groups(authorized_client):
    """Test if can get all groups"""
    response = authorized_client.get("/groups")
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data == expected_groups_response


def test_create_group(authorized_client):
    """Test if can create new group"""
    payload = {"name": "Pytest group name", "description": "Pytest group description"}
    response = authorized_client.post("/groups", json=payload)
    assert response.status_code == 201
    response_data = response.get_json()

    assert response_data == expected_create_group_response


def test_get_single_group(authorized_client):
    """Test if can get a specific group by id"""
    response = authorized_client.get("/groups/1")
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data == expected_single_group_response


def test_update_single_group(authorized_client):
    """Test if can update specific group by id"""
    payload = {"name": "Update group name", "description": "Update group description"}
    response = authorized_client.put("/groups/1", json=payload)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data == expected_update_group_response


def test_can_delete_group(authorized_client):
    """test if can delete specific group by id"""
    response = authorized_client.delete("/groups/1")
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data == expected_delete_group_response
