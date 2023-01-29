from orders_service.serializers.responses import OrderDetailResponseSerializer
from orders_service.serializers.requests import OrderCreateRequestSerializer
from orders_service.exceptions.mappers import OrderMapperException
from orders_service.mappers import OrderMapper
from orders_service.models import Order

from common.exceptions.service import BadRequestException
from common.middlewares import view_wrapper
from common.utils import HttpMethod

from rest_framework.permissions import IsAuthenticated


@view_wrapper(
    http_method_names=[HttpMethod.POST],
    permissions=[IsAuthenticated],
    request_serializer_class=OrderCreateRequestSerializer,
    response_serializer_class=OrderDetailResponseSerializer
)
def create(request_serializer: OrderCreateRequestSerializer) -> Order:
    try:
        return OrderMapper.create(
            payment_method=request_serializer.payment_method,
            delivery_method=request_serializer.delivery_method,
            address=request_serializer.address,
            set_id=request_serializer.set_id,
            user_id=request_serializer.user.id
        )
    except OrderMapperException as e:
        raise BadRequestException(detail=e.args[0])
