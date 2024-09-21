import requests

from common.exceptions.internal import (
    OrdersServiceException,
    UsersServiceException, 
)
from common.dto import (
    BookSetPaginatedList,
    FavoritesList,
    BookSetMap,
    UserData,
)

from uuid import UUID


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
            token=jwt_token,
            id=decoded_response.get("id"),
            name=decoded_response.get("name"),
            email=decoded_response.get("email"),
            surname=decoded_response.get("surname"),
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
            next=decoded_response.get("next_page"),
            previous=decoded_response.get("previous_page"),
            page_size=decoded_response.get("page_size")
        )

    @staticmethod
    def add_to_favorites(jwt_token: str, book_id: UUID) -> bool:
        response = requests.post(
            url=f"{UsersService.BASE_URL}/internal/favorites",
            headers={
                "Authorization": jwt_token
            },
            data={
                "book_id": book_id
            }
        )

        if not response.ok:
            raise UsersServiceException("{}: {}".format(
                UsersServiceException.FAILED_ADD_TO_FAVORITES_MESSAGE,
                response.json().get("detail")
            ))
        
        return True
    
    @staticmethod
    def remove_from_favorites(jwt_token: str, book_id: UUID) -> bool:
        response = requests.delete(
            url=f"{UsersService.BASE_URL}/internal/favorites",
            headers={
                "Authorization": jwt_token
            },
            data={
                "book_id": book_id
            }
        )

        if not response.ok:
            raise UsersServiceException("{}: {}".format(
                UsersServiceException.FAILED_REMOVE_FROM_FAVORITES_MESSAGE,
                response.json().get("detail")
            ))
        
        return True


class OrdersService:
    BASE_URL = "http://localhost:8000/api/v1/orders/internal"

    @staticmethod
    def get_from_bookset(
        jwt_token: str,
        set_id: UUID,
        page: int,
        page_size: int
    ) -> BookSetPaginatedList:
        response = requests.get(
            url=f"{OrdersService.BASE_URL}/book-set/{set_id}",
            headers={
                "Authorization": jwt_token
            },
            params={
                "page": page,
                "page_size": page_size
            }
        )

        if not response.ok:
            raise OrdersServiceException("{}: {}".format(
                    OrdersServiceException.FAILED_GET_FROM_SET,
                    response.json().get("detail")
                ))
        
        decoded_response: dict = response.json()

        return BookSetPaginatedList(
            count=decoded_response.get("count"),
            next_page=decoded_response.get("next_page"),
            previous_page=decoded_response.get("previous_page"),
            page_size=decoded_response.get("page_size"),
            bookset_list=list(map(
                lambda bookset_dict: BookSetMap.from_json(data=bookset_dict),
                decoded_response.get("results")
            ))
        )

    @staticmethod
    def add_to_cart(jwt_token: str, book_id: UUID) -> bool:
        response = requests.post(
            url=f"{OrdersService.BASE_URL}/cart",
            headers={
                "Authorization": jwt_token
            },
            data={
                "book_id": book_id
            }
        )

        if not response.ok:
            raise OrdersServiceException("{}: {}".format(
                OrdersServiceException.FAILED_ADD_TO_CART_MESSAGE,
                response.json().get("detail")
            ))
        
        return True

    @staticmethod
    def remove_from_cart(jwt_token: str, book_id: UUID) -> bool:
        response = requests.delete(
            url=f"{OrdersService.BASE_URL}/cart",
            headers={
                "Authorization": jwt_token
            },
            data={
                "book_id": book_id
            }
        )

        if not response.ok:
            raise OrdersServiceException("{}: {}".format(
                OrdersServiceException.FAILED_REMOVE_FROM_CART_MESSAGE,
                response.json().get("detail")
            ))
        
        return True
