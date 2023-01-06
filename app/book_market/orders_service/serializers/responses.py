from rest_framework.serializers import BaseSerializer
from rest_framework.pagination import DjangoPaginator

from orders_service.serializers.models import (
    DeliveryMethodSerializer,
    PayMethodSerializer,
    BooksetSerializer, 
    OrderSerializer,
)
from orders_service.models import Order

from common.serializers.responses import PaginatedResponseSerializer
from typing import Self


class BooksInBooksetPaginatedResponseSerializer(PaginatedResponseSerializer):
    def __init__(
        self: Self, 
        paginator: DjangoPaginator, 
        page_number: int
    ) -> Self:
        super().__init__(paginator, page_number)
        self.results = BooksetSerializer(
            instance=self.page.object_list,
            many=True
        ).data


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
