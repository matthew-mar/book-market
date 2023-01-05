from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import DjangoPaginator
from rest_framework.response import Response
from rest_framework.request import Request

from common.exceptions.service import BadRequestException, ValidationException
from common.exceptions.internal import DjoserException
from common.services import DjoserService

from orders_service.serializers.responses import (
    BooksInBooksetPaginatedResponseSerializer
)
from orders_service.serializers.requests import (
    BooksetPaginatedListRequestSerializer
)
from orders_service.mappers import BooksetMapper

from uuid import UUID


@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def paginate_bookset(request: Request, set_id: UUID) -> Response:
    try:
        user = DjoserService.me(jwt_token=request.headers.get("Authorization"))
    except DjoserException as e:
        raise BadRequestException(detail=e.args[0])
    
    request_serializer = BooksetPaginatedListRequestSerializer(
        request=request,
        set_id=set_id,
        user_id=user.id
    )

    books = BooksetMapper.find_for_user_in_set(user_id=user.id, set_id=set_id)

    paginator = DjangoPaginator(
        object_list=books,
        per_page=request_serializer.page_size
    )
    if paginator.num_pages < request_serializer.page:
        raise ValidationException(
            detail=f"page number too large max - {paginator.num_pages}"
        )
    
    response_serializer = BooksInBooksetPaginatedResponseSerializer(
        paginator=paginator,
        page_number=request_serializer.page
    )

    return Response(data=response_serializer.data)
