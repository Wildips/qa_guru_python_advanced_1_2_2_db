import faker
import pytest

from http import HTTPStatus

from service_tests.tests.conftest import users
from service_tests.models.reqres import ResponseUser, User

fake = faker.Faker()


def test_users(reqresin):
    response = reqresin.get("/api/users/")
    assert response.status_code == HTTPStatus.OK
    user_list = response.json()["items"]
    for user in user_list:
        ResponseUser(**user)


def test_users_no_duplicates(users):
    users_ids = [int(user["id"]) for user in users["items"]]
    assert len(users_ids) == len(set(users_ids))


def test_user(reqresin, users):
    users_ids = [int(user["id"]) for user in users["items"]]
    for user_id in (users_ids[0], users_ids[-1]):
        response = reqresin.get(f"/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        ResponseUser(**response.json())


def test_user_nonexistent_values(reqresin, users):
    response = reqresin.get(f"/api/users/{len(users["items"]) + 1}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(reqresin, user_id):
    response = reqresin.get(f"/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user(reqresin, random_user_data: User):
    response = reqresin.post("/api/users/", json=random_user_data.json)
    assert response.status_code == HTTPStatus.CREATED
    created_user = User(**response.json())
    assert random_user_data.email == created_user.email
    assert random_user_data.first_name == created_user.first_name
    assert random_user_data.last_name == created_user.last_name
    assert random_user_data.avatar == created_user.avatar
    assert created_user.id
    response = reqresin.get(f"/api/users/{created_user.id}")
    assert response.status_code == HTTPStatus.OK
    checking_user = User(**response.json())
    assert created_user.json == checking_user.json


def test_delete_user(reqresin, random_test_user: User):
    response = reqresin.delete(f"/api/users/{random_test_user.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "User deleted"
    response = reqresin.get(f"/api/users/{random_test_user.id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_update_user(reqresin, create_delete_user: User):
    body = {"email": fake.ascii_free_email(), "first_name": fake.first_name_female(),
            "last_name": fake.last_name_female(), "avatar": fake.uri()}
    response = reqresin.patch(f"/api/users/{create_delete_user.id}", json=body)
    updated_user_data = User(**response.json())
    assert response.status_code == HTTPStatus.OK
    assert updated_user_data.email != create_delete_user.email
    assert updated_user_data.first_name != create_delete_user.first_name
    assert updated_user_data.last_name != create_delete_user.last_name
    assert updated_user_data.avatar != create_delete_user.avatar
    assert updated_user_data.id == create_delete_user.id


def test_update_user_with_nonexistent_id(reqresin, users, random_user_data: User):
    response = reqresin.patch(f"/api/users/{len(users["items"]) + 1}", json=random_user_data.json)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_update_user_with_invalid_id(reqresin, user_id, random_user_data: User):
    response = reqresin.patch(f"/api/users/{user_id}", json=random_user_data.json)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_delete_user_with_nonexistent_id(reqresin, users):
    response = reqresin.delete(f"/api/users/{len(users["items"]) + 1}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "User not found"


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_delete_user_with_invalid_id(reqresin, user_id):
    response = reqresin.delete(f"/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
