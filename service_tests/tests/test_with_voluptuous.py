from pytest_voluptuous import S

from service_tests.schemes.reqres import response_list_users


def test_response_list_users(reqresin):
    response = reqresin.get("/api/users", verify=False)
    assert S(response_list_users) == response.json()
