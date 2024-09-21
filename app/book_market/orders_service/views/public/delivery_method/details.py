from common.serializers.requests import BaseRequestSerializer
from common.middlewares import view_wrapper
from common.utils import HttpMethod

from orders_service.mappers import DeliveryMethodMapper
from orders_service.serializers.responses import (
    DeliveryMethodsResponseSerializer
)
from orders_service.models import DeliveryMethod

from django.db.models import QuerySet


@view_wrapper(
    http_method_names=[HttpMethod.GET],
    request_serializer_class=BaseRequestSerializer,
    response_serializer_class=DeliveryMethodsResponseSerializer
)
def get_delivery_methods(*args) -> QuerySet[DeliveryMethod]:
    return DeliveryMethodMapper.all()
