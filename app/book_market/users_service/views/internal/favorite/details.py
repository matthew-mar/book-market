from common.serializers.requests import PaginationRequestSerializer
from common.middlewares import view_wrapper

from users_service.serializers.responses import (
    FavoritePaginatedResponseSerializer
)
from users_service.mappers import FavoriteMapper
from users_service.mappers import UserMapper
from users_service.models import Favorite

from rest_framework.permissions import IsAuthenticated
from django.db.models import QuerySet


@view_wrapper(
    http_method_names=["GET"],
    permissions=[IsAuthenticated],
    request_serializer_class=PaginationRequestSerializer,
    response_serializer_class=FavoritePaginatedResponseSerializer
)
def paginate(
    request_serializer: PaginationRequestSerializer
) -> QuerySet[Favorite]:
    user = UserMapper.get_by_id(id=request_serializer.user.id)

    return FavoriteMapper.paginate_for_user(user=user)
