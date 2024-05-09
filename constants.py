class Constants:
    URL = "https://stellarburgers.nomoreparties.site"


class Endpoints:
    CREATE_USER = "/api/auth/register"
    DELETE_USER = "/api/auth/user"
    LOGIN = "/api/auth/login"
    GET_USER_DATA = "/api/auth/user"
    CHANGE_USER_DATA = "/api/auth/user"
    CREATE_ORDER = "/api/orders"
    LOGOUT = "/api/auth/logout"


class TextError:
    UNAUTORIZED = "You should be authorised"
    NO_PROVIDED_INGR = "Ingredient ids must be provided"
    EXISTING_USER = "User already exists"
    REQUIRED_FIELD = "Email, password and name are required fields"
    INCORRECT = "email or password are incorrect"
