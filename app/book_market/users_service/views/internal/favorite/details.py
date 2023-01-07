from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import DjangoPaginator
from rest_framework.response import Response
from rest_framework.request import Request

from common.serializers.requests import PaginationRequestSerializer
from common.exceptions.service import ValidationException
from common.services import UsersService

from users_service.mappers import UserMapper, FavoriteMapper
from users_service.serializers.responses import (
    FavoritePaginatedResponseSerializer
)


@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def paginate(request: Request) -> Response:
    request_serializer = PaginationRequestSerializer(request=request)

    user_data = UsersService.me(
        jwt_token=request.headers.get("Authorization")
    )

    user = UserMapper.get_by_id(id=user_data.id)

    favorites = FavoriteMapper.paginate_for_user(user=user)

    paginator = DjangoPaginator(
        object_list=favorites,
        per_page=request_serializer.page_size
    )
    
    if paginator.num_pages < request_serializer.page:
        raise ValidationException(
            detail=f"page number too large, max - {paginator.num_pages}"
        )
    
    response_serializer = FavoritePaginatedResponseSerializer(
        paginator=paginator,
        page_number=request_serializer.page
    )

    return Response(data=response_serializer.data)
