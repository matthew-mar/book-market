from rest_framework.serializers import BaseSerializer
from rest_framework.request import Request

from common.exceptions.service import ValidationException
from typing import Self


class PaginationRequestSerializer(BaseSerializer):
    def __init__(self: Self, request: Request) -> Self:
        self.request = request
        self.validate()
    
    def validate(self: Self):
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
