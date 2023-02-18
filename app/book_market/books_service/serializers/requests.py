from common.serializers.requests import PaginationRequestSerializer
from common.exceptions.service import ValidationException
from common.utils import is_valid_uuid

from rest_framework.request import Request
from typing import Self


class BooksFilterRequestSerializer(PaginationRequestSerializer):
    order: str
    
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
                detail="order must be string and one of (asc, desc)"
            )
        
        if order not in ("asc", "desc"):
            raise ValidationException(detail="order can only be asc or desc")

        match order:
            case "asc":
                self.order = ""
            case "desc":
                self.order = "-"


class PaginatedSetRequestSerializer(PaginationRequestSerializer):
    set_id: str

    def __init__(self: Self, request: Request) -> Self:
        super().__init__(request)
    
    def validate(self: Self) -> None:
        super().validate()

        set_id = self.request.data.get("set_id")

        if set_id is None:
            raise ValidationException(detail="set_id is required")
        
        if not is_valid_uuid(value=set_id):
            raise ValidationException(
                detail=f"set_id value ({set_id}) is not a valid uuid"
            )
        
        self.set_id = set_id
