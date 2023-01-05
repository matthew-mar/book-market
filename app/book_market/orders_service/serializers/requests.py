from common.serializers.requests import PaginationRequestSerializer
from common.exceptions.service import NotFoundException

from orders_service.mappers import BooksetMapper
from rest_framework.request import Request
from typing import Self
from uuid import UUID


class BooksetPaginatedListRequestSerializer(PaginationRequestSerializer):
    def __init__(
        self: Self, 
        request: Request, 
        set_id: UUID, 
        user_id: UUID
    ) -> Self:
        self.user_id = user_id
        self.set_id = set_id
        super().__init__(request)
    
    def validate(self: Self) -> None:
        print(self.set_id)
        super().validate()

        books_in_set_count = BooksetMapper.count_for_user_in_set(
            user_id=self.user_id,
            set_id=self.set_id
        )
        if books_in_set_count == 0:
            raise NotFoundException(detail=f"set_id {self.set_id} not exist")
