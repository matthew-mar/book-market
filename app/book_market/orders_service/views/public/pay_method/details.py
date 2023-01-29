from orders_service.mappers import PayMethodMapper
from orders_service.serializers.responses import (
    PaymentMethodsResponseSerializer
)
from orders_service.models import PayMethod

from common.middlewares import view_wrapper
from common.utils import HttpMethod

from django.db.models import QuerySet


@view_wrapper(
    http_method_names=[HttpMethod.GET],
    response_serializer_class=PaymentMethodsResponseSerializer
)
def get_payment_methods(*args) -> QuerySet[PayMethod]:
    return PayMethodMapper.all()
