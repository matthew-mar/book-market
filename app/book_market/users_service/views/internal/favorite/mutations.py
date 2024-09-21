from users_service.exceptions.mappers import FavoriteMapperException
from users_service.mappers import FavoriteMapper, UserMapper

from common.serializers.responses import SuccessResponseSerializer
from common.serializers.requests import ForBookRequestSerializer
from common.exceptions.service import BadRequestException
from common.middlewares import view_wrapper
from common.utils import HttpMethod

from rest_framework.permissions import IsAuthenticated


@view_wrapper(
    http_method_names=[HttpMethod.POST, HttpMethod.DELETE],
    permissions=[IsAuthenticated],
    request_serializer_class=ForBookRequestSerializer,
    response_serializer_class=SuccessResponseSerializer
)
def favorites_controller(request_serializer: ForBookRequestSerializer) -> bool:
    user = UserMapper.get_by_id(id=request_serializer.user.id)

    try:
        match request_serializer.request.method:
            case HttpMethod.POST:
                return FavoriteMapper.create(
                    user=user,
                    book_id=request_serializer.book_id
                )
            case HttpMethod.DELETE:
                return FavoriteMapper.delete(
                    user=user,
                    book_id=request_serializer.book_id
                )
    except FavoriteMapperException as e:
        raise BadRequestException(detail=e.args[0])
