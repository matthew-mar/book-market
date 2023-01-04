from common.exceptions.service import ValidationException
from common.utils import is_valid_uuid

from rest_framework.serializers import Serializer
from rest_framework.request import Request

from accessify import private
from typing import Any, Self
from uuid import UUID


class FavoriteCreateRequestSerialzier(Serializer):
    def __init__(self: Self, requrest: Request) -> Self:
        self.request = requrest
        self.validate()

    @private
    def validate_book_id(self: Self, value: Any) -> UUID:
        if value is None:
            raise ValidationException(detail="book_id is required")
        
        if not is_valid_uuid(object=value):
            raise ValidationException(
                detail=f"book_id value ({value}) is not a valid uuid string" 
            )
        
        return value
    
    @private
    def validate(self: Self) -> None:
        self.book_id = self.validate_book_id(
            value=self.request.data.get("book_id")
        )
