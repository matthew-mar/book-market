from common.serializers.responses import SuccessResponseSerializer
from common.serializers.requests import ForBookRequestSerializer
from common.exceptions.service import BadRequestException
from common.middlewares import view_wrapper
from common.utils import HttpMethod

from orders_service.exceptions.mappers import CartMapperException
from orders_service.mappers import CartMapper

from rest_framework.permissions import IsAuthenticated


@view_wrapper(
    http_method_names=[HttpMethod.PATCH],
    permissions=[IsAuthenticated],
    request_serializer_class=ForBookRequestSerializer,
    response_serializer_class=SuccessResponseSerializer
)
def increase(request_serializer: ForBookRequestSerializer) -> bool:
    try:
        return CartMapper.increase_book_amount(
            user_id=request_serializer.user.id,
            book_id=request_serializer.book_id
        )
    except CartMapperException as e:
        raise BadRequestException(detail=e.args[0])


@view_wrapper(
    http_method_names=[HttpMethod.PATCH],
    permissions=[IsAuthenticated],
    request_serializer_class=ForBookRequestSerializer,
    response_serializer_class=SuccessResponseSerializer
)
def decrease(request_serializer: ForBookRequestSerializer) -> bool:
    try:
        return CartMapper.decrease_book_amount(
            user_id=request_serializer.user.id,
            book_id=request_serializer.book_id
        )
    except CartMapperException as e:
        raise BadRequestException(detail=e.args[0])
