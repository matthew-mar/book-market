from rest_framework.serializers import BaseSerializer
from rest_framework.pagination import DjangoPaginator

from common.serializers.requests import PaginationRequestSerializer
from common.serializers.requests import BaseRequestSerializer
from common.exceptions.service import ValidationException
from common.data_models import PaginatedResponse

from typing import Self, Any
from abc import ABC


class BaseResponseSerializer(ABC, BaseSerializer):
    def __init__(
        self: Self, 
        request_serializer: BaseRequestSerializer,
        result: Any
    ) -> Self:
        self.request_serializer = request_serializer
        self.result = result

    @property
    def data(self: Self) -> dict | list:
        return self.result


class SuccessResponseSerializer(BaseResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: BaseRequestSerializer, 
        result: bool
    ) -> Self:
        super().__init__(request_serializer, result)
    
    @property
    def data(self: Self) -> dict:
        return {
            "success": self.result
        }


class PaginatedResponseSerializer(BaseResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: PaginationRequestSerializer, 
        result: Any
    ) -> Self:
        super().__init__(request_serializer, result)
    
    @property
    def data(self: Self) -> dict:
        paginator = DjangoPaginator(
            object_list=self.result, 
            per_page=self.request_serializer.page_size
        )

        if paginator.num_pages < self.request_serializer.page:
            raise ValidationException(
                detail=f"page number too large, max - {paginator.num_pages}"
            )

        page = paginator.get_page(number=self.request_serializer.page)
        next_page = (
            None if not page.has_next() 
            else page.next_page_number()
        )
        previous_page = (
            None if not page.has_previous()
            else page.previous_page_number()
        )

        return PaginatedResponse(
            count=paginator.count,
            next_page=next_page,
            previous_page=previous_page,
            page_size=paginator.per_page,
            results=page.object_list
        ).json
