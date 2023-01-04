import requests

from common.exceptions.internal import DjoserException
from common.data_models import UserData


class DjoserService:
    BASE_URL = "http://localhost:8000/api/v1/users"

    @staticmethod
    def me(jwt_token: str) -> UserData:
        response = requests.get(
            url=f"{DjoserService.BASE_URL}/me",
            headers={
                "Authorization": jwt_token
            }
        )

        if not response.ok:
            DjoserException.failed_get_user()

        decoded_response: dict = response.json()

        return UserData(
            id=decoded_response.get("id"),
            name=decoded_response.get("name"),
            surname=decoded_response.get("surname"),
            email=decoded_response.get("email"),
            phone_number=decoded_response.get("phone_number")
        )
