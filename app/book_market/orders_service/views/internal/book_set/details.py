from common.middlewares import view_wrapper
from common.utils import HttpMethod

from orders_service.serializers.responses import (
    BooksInBooksetPaginatedResponseSerializer
)
from orders_service.serializers.requests import (
    BooksetPaginatedListRequestSerializer
)
from orders_service.mappers import BooksetMapper
from orders_service.models import Bookset

from rest_framework.permissions import IsAuthenticated
from django.db.models import QuerySet
from uuid import UUID


@view_wrapper(
    http_method_names=[HttpMethod.GET],
    permissions=[IsAuthenticated],
    request_serializer_class=BooksetPaginatedListRequestSerializer,
    response_serializer_class=BooksInBooksetPaginatedResponseSerializer
)
def paginate_bookset(
    request_serializer: BooksetPaginatedListRequestSerializer,
    set_id: UUID
) -> QuerySet[Bookset]:
    return BooksetMapper.find_for_user_in_set(
        user_id=request_serializer.user.id,
        set_id=set_id
    )
