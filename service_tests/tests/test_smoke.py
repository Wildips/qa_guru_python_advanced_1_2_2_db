from http import HTTPStatus


def test_app_status(reqresin):
    response = reqresin.get("/status/")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["database"], "Init data are absent"
