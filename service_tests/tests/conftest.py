import json
import pytest
import faker

from http import HTTPStatus
from pathlib import Path

from service_tests.models.reqres import User

fake = faker.Faker()


@pytest.fixture(scope="session", autouse=True)
def fill_test_data(reqresin):
    with open(Path(__file__).parent.parent.parent.joinpath("users.json").absolute()) as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        api_users.append(User(**reqresin.post(f"/api/users", json=user).json()))
    user_ids = [user.id for user in api_users]

    yield user_ids

    for user_id in user_ids:
        reqresin.delete(f"/api/users/{user_id}")


@pytest.fixture
def users(reqresin):
    response = reqresin.get("/api/users/")
    return response.json()


@pytest.fixture()
def random_user_data() -> User:
    user = User(email=fake.ascii_free_email(), first_name=fake.first_name_female(), last_name=fake.last_name_female(),
                avatar=fake.uri())
    return user


@pytest.fixture()
def random_test_user(random_user_data: User, reqresin) -> User:
    response = reqresin.post("/api/users/", json=random_user_data.json)
    return User(**response.json())


@pytest.fixture()
def create_delete_user(random_user_data: User, reqresin) -> User:
    response = reqresin.post("/api/users/", json=random_user_data.json)
    assert response.status_code == HTTPStatus.CREATED
    random_user_data = User(**response.json())
    yield random_user_data
    response = reqresin.delete(f"/api/users/{response.json()["id"]}")
    assert response.status_code == HTTPStatus.OK
