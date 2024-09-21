from common.serializers.responses import SuccessResponseSerializer
from common.serializers.requests import ForBookRequestSerializer
from common.exceptions.service import BadRequestException
from common.middlewares import view_wrapper
from common.utils import HttpMethod

from orders_service.exceptions.mappers import CartMapperException
from orders_service.mappers import CartMapper

from rest_framework.permissions import IsAuthenticated


@view_wrapper(
    http_method_names=[HttpMethod.POST, HttpMethod.DELETE],
    permissions=[IsAuthenticated],
    request_serializer_class=ForBookRequestSerializer,
    response_serializer_class=SuccessResponseSerializer
)
def cart_controller(request_resializer: ForBookRequestSerializer) -> bool:
    try:
        match request_resializer.request.method:
            case HttpMethod.POST:
                return CartMapper.add_or_create(
                    user_id=request_resializer.user.id,
                    book_id=request_resializer.book_id
                )
            case HttpMethod.DELETE:
                return CartMapper.delete_book_from_cart(
                    user_id=request_resializer.user.id,
                    book_id=request_resializer.book_id
                )
    except CartMapperException as e:
        raise BadRequestException(detail=e.args[0])
