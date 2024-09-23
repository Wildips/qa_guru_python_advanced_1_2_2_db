from service_tests.models.reqres import ResponseUser, Reqres


def test_get_user(reqresin):
    expected_response_get_user = ResponseUser(
        id=2,
        email="janet.weaver@reqres.in",
        first_name="Janet",
        last_name="Weaver",
        avatar="https://reqres.in/img/faces/2-image.jpg",
    )

    result_response_get_user = ResponseUser(response=reqresin.get("/api/users/2"))

    assert result_response_get_user.json["id"] == expected_response_get_user.json["id"]
    assert result_response_get_user.json["email"] == expected_response_get_user.json["email"]
    assert result_response_get_user.json["first_name"] == expected_response_get_user.json["first_name"]
    assert result_response_get_user.json["last_name"] == expected_response_get_user.json["last_name"]
    assert result_response_get_user.json["avatar"] == expected_response_get_user.json["avatar"]


def test_get_user_with_object_model(env):
    expected_response_get_user = ResponseUser(
        id=2,
        email="janet.weaver@reqres.in",
        first_name="Janet",
        last_name="Weaver",
        avatar="https://reqres.in/img/faces/2-image.jpg",
    )

    result_response_get_user = Reqres(env).get_user(2)

    assert result_response_get_user.json == expected_response_get_user.json
