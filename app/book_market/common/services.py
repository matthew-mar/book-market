import requests

from common.exceptions.internal import UsersServiceException
from common.data_models import UserData, FavoritesList


class UsersService:
    BASE_URL = "http://localhost:8000/api/v1/users"

    @staticmethod
    def me(jwt_token: str) -> UserData:
        response = requests.get(
            url=f"{UsersService.BASE_URL}/me",
            headers={
                "Authorization": jwt_token
            }
        )

        if not response.ok:
            UsersServiceException.failed_get_user()

        decoded_response: dict = response.json()

        return UserData(
            id=decoded_response.get("id"),
            name=decoded_response.get("name"),
            surname=decoded_response.get("surname"),
            email=decoded_response.get("email"),
            phone_number=decoded_response.get("phone_number")
        )
    
    @staticmethod
    def get_from_favorites(
        jwt_token: str, 
        page: int, 
        page_size: int
    ) -> FavoritesList:
        response = requests.get(
            url=f"{UsersService.BASE_URL}/internal/favorites/list",
            headers={
                "Authorization": jwt_token
            },
            params={
                "page": page,
                "page_size": page_size
            }
        )

        if not response.ok:
            raise UsersServiceException("{}: {}".format(
                UsersServiceException.FAILED_GET_FAVORITES,
                response.json().get("detail")
            ))
        
        decoded_response: dict = response.json()

        return FavoritesList(
            books=decoded_response.get("results"),
            count=decoded_response.get("count"),
            next=decoded_response.get("next"),
            previous=decoded_response.get("previous"),
            page_size=decoded_response.get("page_size")
        )
