import pytest
import requests
import random
import string

from constants import Constants, Endpoints


@pytest.fixture
def create_payload():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
    email = generate_random_string(5) + "@yandex.ru"
    password = generate_random_string(10)
    name = generate_random_string(10)
    payload = {"email": email, "password": password, "name": name}
    yield payload


@pytest.fixture
def create_user_then_delete_user(create_payload):
    resp_create = requests.post(f"{Constants.URL}{Endpoints.CREATE_USER}",
                                data=create_payload)
    token_with_bearer = resp_create.json()["accessToken"]
    user_token = token_with_bearer.split()
    token = user_token[1]
    payload_login = {}
    payload_login.update(create_payload)
    del payload_login["name"]
    fix = [payload_login, token, create_payload, token_with_bearer]
    yield fix
    response_del = requests.delete(f"{Constants.URL}{Endpoints.DELETE_USER}",
                                   headers={'Authorization': token_with_bearer})


@pytest.fixture
def create_user_and_order_then_delete_user(create_user_then_delete_user):
    payload_order = {"ingredients": ["61c0c5a71d1f82001bdaaa6d",
                                     "61c0c5a71d1f82001bdaaa70",
                                     "61c0c5a71d1f82001bdaaa72"]}
    resp_order = requests.post(f"{Constants.URL}{Endpoints.CREATE_ORDER}",
                               headers={"Authorization": create_user_then_delete_user[1]},
                               data=payload_order)
    yield create_user_then_delete_user[3]
    response_del = requests.delete(f"{Constants.URL}{Endpoints.DELETE_USER}",
                                   headers={'Authorization': create_user_then_delete_user[3]})