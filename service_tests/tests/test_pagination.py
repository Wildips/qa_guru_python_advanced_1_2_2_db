import pytest

from http import HTTPStatus

from service_tests.utils.utils import pages_count


def test_users_pagination_page(reqresin, users):
    size = 1
    response = reqresin.get(f"/api/users/?size={size}&page={len(users["items"])}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["total"] == len(users["items"])
    assert response.json()["page"] == len(users["items"])
    assert response.json()["size"] == size
    assert response.json()["pages"] == len(users["items"])
    assert len(response.json()) == 5


def test_users_pagination_size(reqresin, users):
    page = 1
    size = 100
    response = reqresin.get(f"/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["total"] == len(users["items"])
    assert response.json()["page"] == pages_count(len(users["items"]), size)
    assert response.json()["size"] == size
    assert response.json()["pages"] == pages_count(len(users["items"]), size)
    assert len(response.json()) == 5


@pytest.mark.parametrize("page", [-1, 0, "fafaf"])
def test_invalid_page(reqresin, page):
    size = 1
    response = reqresin.get(f"/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("size", [-1, 0, "fafaf"])
def test_invalid_size(reqresin, size):
    page = 1
    response = reqresin.get(f"/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_nonexistent_page(reqresin, users):
    size = 1
    response = reqresin.get(f"/api/users/?size={size}&page={len(users["items"]) + 1}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["page"] == len(users["items"]) + 1
    assert response.json()["size"] == size
    assert response.json()["pages"] == response.json()["total"]
    assert response.json()["items"] == []
    assert len(response.json()) == 5


def test_nonexistent_size(reqresin):
    page = 1
    size = 999
    response = reqresin.get(f"/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_different_results_on_different_pages(reqresin, users):
    size = 1
    page = 1
    first_page_response = reqresin.get(f"/api/users/?size={size}&page={page}")
    second_page_response = reqresin.get(f"/api/users/?size={size}&page={page + 1}")
    assert first_page_response.json()["items"] != second_page_response.json()["items"]
