from common.serializers.responses import PaginatedResponseSerializer
from common.serializers.requests import PaginationRequestSerializer

from orders_service.serializers.models import (
    BooksetSerializer, 
    OrderSerializer,
)
from orders_service.models import Bookset

from rest_framework.pagination import DjangoPaginator
from django.db.models import QuerySet
from typing import Self


class BooksInBooksetPaginatedResponseSerializer(PaginatedResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: PaginationRequestSerializer, 
        result: QuerySet[Bookset]
    ) -> Self:
        super().__init__(request_serializer, result)

        self.result = BooksetSerializer(instance=result, many=True).data


class OrderInPaginatedListResponseSerializer(PaginatedResponseSerializer):
    def __init__(
        self: Self,
        paginator: DjangoPaginator,
        page_number: int
    ) -> Self:
        super().__init__(paginator=paginator, page_number=page_number)
        self.results = OrderSerializer(
            instance=self.page.object_list,
            many=True
        ).data
