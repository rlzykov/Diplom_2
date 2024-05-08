import requests
import allure
from constants import Constants, Endpoints, TextError


class TestGetOrdersOfUser:
    @allure.title("Можно получить список заказов конкретного юзера")
    def test_get_users_orders_orders_got(self, create_user_and_order_then_delete_user):
        response = requests.get(f"{Constants.URL}{Endpoints.CREATE_ORDER}",
                                headers={"Authorization": create_user_and_order_then_delete_user})
        assert response.status_code == 200
        assert "orders" in response.json()

    @allure.title("Нельзя получить список заказов без авторизации")
    def test_get_users_orders_without_authorization_not_get(self, create_user_and_order_then_delete_user):
        response = requests.get(f"{Constants.URL}{Endpoints.CREATE_ORDER}")
        assert response.status_code == 401
        assert response.json()["message"] == TextError.UNAUTORIZED
