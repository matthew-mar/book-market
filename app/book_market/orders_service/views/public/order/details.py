from common.exceptions.service import BadRequestException
from common.middlewares import view_wrapper
from common.serializers.requests import (
    PaginationRequestSerializer,
    BaseRequestSerializer,
)
from common.utils import HttpMethod

from orders_service.serializers.responses import OrderDetailResponseSerializer
from orders_service.exceptions.mappers import OrderMapperException
from orders_service.serializers.responses import (
    OrderInPaginatedListResponseSerializer
)
from orders_service.mappers import OrderMapper
from orders_service.models import Order

from rest_framework.permissions import IsAuthenticated
from django.db.models import QuerySet
from uuid import UUID


@view_wrapper(
    http_method_names=[HttpMethod.GET],
    permissions=[IsAuthenticated],
    response_serializer_class=OrderDetailResponseSerializer
)
def detail(request_serializer: BaseRequestSerializer, order_id: UUID) -> Order:
    try:
        return OrderMapper.get_for_user_by_id(
            user_id=request_serializer.user.id,
            id=order_id
        )
    except OrderMapperException as e:
        raise BadRequestException(detail=e.args[0])


@view_wrapper(
    http_method_names=[HttpMethod.GET],
    permissions=[IsAuthenticated],
    request_serializer_class=PaginationRequestSerializer,
    response_serializer_class=OrderInPaginatedListResponseSerializer
)
def paginate(
    request_serializer: PaginationRequestSerializer
) -> QuerySet[Order]:
    try:
        return OrderMapper.find_for_user(user_id=request_serializer.user.id)
    except OrderMapperException as e:
        raise BadRequestException(detail=e.args[0])
