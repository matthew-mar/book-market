from common.serializers.responses import PaginatedResponseSerializer
from rest_framework.serializers import BaseSerializer
from rest_framework.pagination import DjangoPaginator

from orders_service.serializers.models import (
    DeliveryMethodSerializer,
    PayMethodSerializer,
    BooksetSerializer, 
    OrderSerializer,
)
from orders_service.models import Order

from datetime import datetime
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


class OrderDetailSerializer(BaseSerializer):
    def __init__(
        self: Self, 
        order: Order
    ) -> Self:
        self.order = order
    
    @property
    def data(self: Self):
        data = OrderSerializer(self.order).data
        data["payment_method"] = PayMethodSerializer(
            instance=self.order.payment_method
        ).data
        data["delivery_method"] = DeliveryMethodSerializer(
            instance=self.order.delivery_method
        ).data
        return data
