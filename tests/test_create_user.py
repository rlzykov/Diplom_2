import requests
import allure
from constants import Constants, Endpoints, TextError
from faker import Faker

faker = Faker()


class TestCreateUser:
    @allure.title("Пользователя можно создать")
    def test_new_user_created(self, create_payload):
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_USER}",
                                 data=create_payload)
        token_with_bearer = response.json()["accessToken"]
        response_del = requests.delete(f"{Constants.URL}{Endpoints.DELETE_USER}",
                                       headers={'Authorization': token_with_bearer})
        assert response.status_code == 200
        assert response.json()["success"] == True

    @allure.title("Нельзя создать пользователя, который уже зарегистрирован")
    def test_the_same_user_not_created(self, create_payload):
        resp_first = requests.post(f"{Constants.URL}{Endpoints.CREATE_USER}",
                                   data=create_payload)
        token_with_bearer = resp_first.json()["accessToken"]
        resp_second = requests.post(f"{Constants.URL}{Endpoints.CREATE_USER}",
                                    data=create_payload)
        response_del = requests.delete(f"{Constants.URL}{Endpoints.DELETE_USER}",
                                       headers={'Authorization': token_with_bearer})
        assert resp_second.status_code == 403
        assert resp_second.json()["message"] == TextError.EXISTING_USER

    @allure.title("Нельзя создать пользователя без email")
    def test_user_without_email_not_created(self):
        payload = {"email": "",
                   "password": faker.password,
                   "name": faker.first_name}
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_USER}",
                                 data=payload)
        assert response.status_code == 403
        assert response.json()["message"] == TextError.REQUIRED_FIELD

    @allure.title("Нельзя создать пользователя без пароля")
    def test_user_without_password_not_created(self):
        payload = {"email": faker.email,
                   "password": "",
                   "name": faker.first_name}
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_USER}",
                                 data=payload)
        assert response.status_code == 403
        assert response.json()["message"] == TextError.REQUIRED_FIELD

    @allure.title("Нельзя создать пользователя без имени")
    def test_user_without_name_not_created(self):
        payload = {"email": faker.email,
                   "password": faker.password,
                   "name": ""}
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_USER}",
                                 data=payload)
        assert response.status_code == 403
        assert response.json()["message"] == TextError.REQUIRED_FIELD
