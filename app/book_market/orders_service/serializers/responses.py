from common.serializers.responses import (
    PaginatedResponseSerializer, 
    BaseResponseSerializer,
)
from common.serializers.requests import (
    PaginationRequestSerializer, 
    BaseRequestSerializer,
)

from orders_service.models import Bookset, DeliveryMethod, Order, PayMethod
from orders_service.serializers.models import (
    BooksetInPaginationListSerializer, 
    DeliveryMethodSerializer,
    PayMethodSerializer,
    OrderSerializer,
)

from django.db.models import QuerySet
from typing import Self


class BooksInBooksetPaginatedResponseSerializer(PaginatedResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: PaginationRequestSerializer, 
        result: QuerySet[Bookset]
    ) -> Self:
        super().__init__(request_serializer, result)

        self.result = BooksetInPaginationListSerializer(
            instance=result, 
            many=True
        ).data


class DeliveryMethodsResponseSerializer(BaseResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: BaseRequestSerializer, 
        result: QuerySet[DeliveryMethod]
    ) -> Self:
        super().__init__(request_serializer, result)

        self.result = DeliveryMethodSerializer(instance=result, many=True).data


class OrderDetailResponseSerializer(BaseResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: BaseRequestSerializer, 
        result: Order
    ) -> Self:
        super().__init__(request_serializer, result)

        self.result = OrderSerializer(instance=result).data


class OrderInPaginatedListResponseSerializer(PaginatedResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: PaginationRequestSerializer, 
        result: QuerySet[Order]
    ) -> Self:
        super().__init__(request_serializer, result)

        self.result = OrderSerializer(instance=result, many=True).data


class PaymentMethodsResponseSerializer(BaseResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: BaseRequestSerializer, 
        result: QuerySet[PayMethod]
    ) -> Self:
        super().__init__(request_serializer, result)

        self.result = PayMethodSerializer(instance=result, many=True).data
