from common.serializers.requests import PaginationRequestSerializer
from common.exceptions.service import ValidationException

from rest_framework.request import Request
from typing import Self


class BooksFilterRequestSerializer(PaginationRequestSerializer):
    def __init__(self: Self, request: Request) -> Self:
        super().__init__(request)

    def validate(self: Self) -> None:
        super().validate()

        order = self.request.query_params.get("order")

        if order is None:
            self.order = ""
            return
        
        if not isinstance(order, str):
            raise ValidationException(
                detail="order must be string one of (asc, desc)"
            )
        
        if order not in ("asc", "desc"):
            raise ValidationException(detail="order can be only asc or desc")
        
        match order:
            case "asc":
                self.order = ""
            case "desc":
                self.order = "-"
