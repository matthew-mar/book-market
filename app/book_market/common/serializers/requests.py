from rest_framework.serializers import BaseSerializer
from rest_framework.request import Request

from common.exceptions.service import ValidationException
from common.utils import is_valid_uuid

from accessify import private
from typing import Self, Any
from uuid import UUID


class PaginationRequestSerializer(BaseSerializer):
    def __init__(self: Self, request: Request) -> Self:
        self.request = request
        self.validate()
    
    def validate(self: Self) -> None:
        params = {
            "page": self.request.query_params.get("page"),
            "page_size": self.request.query_params.get("page_size")
        }

        for param in params:
            value = params[param]

            if not value:
                raise ValidationException(detail=f"{param} is required")
            
            if ((not isinstance(value, str)) or 
                (isinstance(value, str) and not value.isdigit())
            ):
                raise ValidationException(detail=f"{param} must be an integer")
            
            params[param] = int(value)

            if params[param] < 1:
                raise ValidationException(
                    detail=f"{param} can't be less than 1"
                )

        self.page, self.page_size = params.values()


class ForBookRequestSerializer(BaseSerializer):
    def __init__(self: Self, requrest: Request) -> Self:
        self.request = requrest
        self.validate()

    @private
    def validate_book_id(self: Self, value: Any) -> UUID:
        if value is None:
            raise ValidationException(detail="book_id is required")
        
        if not is_valid_uuid(value=value):
            raise ValidationException(
                detail=f"book_id value ({value}) is not a valid uuid string" 
            )
        
        return value
    
    @private
    def validate(self: Self) -> None:
        self.book_id = self.validate_book_id(
            value=self.request.data.get("book_id")
        )
