import requests
import allure
from constants import Constants, Endpoints, TextError


class TestCreateOrder:
    @allure.title("Авторизованный пользователь может создать заказ")
    def test_create_order_by_authorized_user_order_created(self, create_user_then_delete_user):
        payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6d",
                                   "61c0c5a71d1f82001bdaaa70",
                                   "61c0c5a71d1f82001bdaaa72"]}
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_ORDER}",
                                 headers={"Authorization": f"Bearer {create_user_then_delete_user[1]}"},
                                 data=payload)
        assert response.status_code == 200
        assert "order" in response.json()

    @allure.title("Неавторизованный пользователь не может создать заказ")
    def test_create_order_by_unauthorized_user_order_not_created(self):
        payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6d",
                                   "61c0c5a71d1f82001bdaaa70",
                                   "61c0c5a71d1f82001bdaaa72"]}
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_ORDER}", data=payload)
        assert response.status_code == 200

    @allure.title("Авторизованный пользователь не может создать заказ без ингредиентов")
    def test_create_order_by_authorized_user_without_ingrds_order_not_created(self, create_user_then_delete_user):
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_ORDER}",
                                 headers={"Authorization": f"Bearer {create_user_then_delete_user[1]}"})
        assert response.status_code == 400
        assert response.json()["message"] == TextError.NO_PROVIDED_INGR

    @allure.title("Авторизованный пользователь не может создать заказ с неверным хешем ингредиентов")
    def test_create_order_by_authorized_user_with_invalid_ingrds_order_not_created(self, create_user_then_delete_user):
        payload = {"ingredients": ["61c0c5a7155555",
                                   "",
                                   "123456"]}
        response = requests.post(f"{Constants.URL}{Endpoints.CREATE_ORDER}",
                                 headers={"Authorization": f"Bearer {create_user_then_delete_user[1]}"},
                                 data=payload)
        assert response.status_code == 500
