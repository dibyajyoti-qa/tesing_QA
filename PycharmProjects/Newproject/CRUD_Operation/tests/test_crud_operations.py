import requests
import pytest
import json

# Base URL for the API
BASE_URL = "https://crudcrud.com/api/91c381b4d77a42ae9b8c6f538ca3e16b/users"


@pytest.fixture
def new_user_data():
    """Fixture to provide data for creating a new user."""
    return {
        "name": "Bikash Jena",
        "email": "bikash.jena@example.com",
        "age": 29
    }


@pytest.fixture
def create_user(new_user_data):
    """Fixture to create a new user and return the user data."""
    response = requests.post(BASE_URL, json=new_user_data)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    user_data = response.json()
    assert "_id" in user_data, "Response does not contain an '_id' field"

    # Store the user id for later tests
    new_user_data["id"] = user_data["_id"]
    return new_user_data


def test_create_user(create_user):
    """Test case to create a new user."""
    # Since the user is created in the fixture, no need to do anything else in this test.
    assert "id" in create_user, "User creation failed: No 'id' found"


def test_get_user(create_user):
    """Test case to get a user by ID."""
    user_id = create_user.get("id")
    response = requests.get(f"{BASE_URL}/{user_id}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    user_data = response.json()
    assert user_data["name"] == create_user["name"], "User name does not match"
    assert user_data["email"] == create_user["email"], "User email does not match"
    assert user_data["age"] == create_user["age"], "User age does not match"


def test_update_user(create_user):
    """Test case to update an existing user."""
    user_id = create_user.get("id")
    update_user_data = {
        "name": "Paresh Samal",
        "email": "paresh.samal@example.com",
        "age": 30
    }

    # Perform the PUT request to update the user
    response = requests.put(f"{BASE_URL}/{user_id}", json=update_user_data)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Print the response content to inspect it
    print(f"Response Content: {response.text}")

    # Try to parse JSON if it's available
    try:
        updated_user = response.json()
    except requests.exceptions.JSONDecodeError:
        updated_user = None
        print("No JSON returned in response.")

    # If JSON is returned, check the updated user details
    if updated_user:
        assert updated_user["name"] == update_user_data["name"], "User name was not updated correctly"
        assert updated_user["email"] == update_user_data["email"], "User email was not updated correctly"
        assert updated_user["age"] == update_user_data["age"], "User age was not updated correctly"
    else:
        # If no content is returned, we can perform a GET request to retrieve the updated user.
        response = requests.get(f"{BASE_URL}/{user_id}")
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        # Verify that the user data was updated
        updated_user_data = response.json()
        assert updated_user_data["name"] == update_user_data["name"], "User name was not updated correctly"
        assert updated_user_data["email"] == update_user_data["email"], "User email was not updated correctly"
        assert updated_user_data["age"] == update_user_data["age"], "User age was not updated correctly"


def test_delete_user(create_user):
    """Test case to delete a user by ID."""
    user_id = create_user.get("id")
    response = requests.delete(f"{BASE_URL}/{user_id}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Verify the user was deleted by attempting to retrieve it
    response = requests.get(f"{BASE_URL}/{user_id}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"