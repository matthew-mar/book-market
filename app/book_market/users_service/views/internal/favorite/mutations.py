from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from users_service.exceptions.mappers import FavoriteMapperException
from users_service.mappers import FavoriteMapper, UserMapper
from users_service.serializers.requests import (
    FavoriteMutationRequestSerializer
)

from common.serializers.responses import SuccessResponseSerializer
from common.exceptions.service import BadRequestException
from common.services import DjoserService


@api_view(http_method_names=["POST", "DELETE"])
@permission_classes(permission_classes=[IsAuthenticated])
def favorites_controller(request: Request) -> Response:
    match (request.method):
        case "POST":
            return add_to_favorites(request=request)
        case "DELETE":
            return remove_from_favorites(request=request)


def add_to_favorites(request: Request) -> Response:
    request_serializer = FavoriteMutationRequestSerializer(requrest=request)

    user_data = DjoserService.me(
        jwt_token=request.headers.get("Authorization")
    )

    user = UserMapper.get_by_id(id=user_data.id)

    try:
        result = FavoriteMapper.create(
            user=user, 
            book_id=request_serializer.book_id
        )
    except FavoriteMapperException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=SuccessResponseSerializer(result=result).data)


def remove_from_favorites(request: Request) -> Response:
    request_serializer = FavoriteMutationRequestSerializer(requrest=request)

    user_data = DjoserService.me(
        jwt_token=request.headers.get("Authorization")
    )

    user = UserMapper.get_by_id(id=user_data.id)

    try:
        result = FavoriteMapper.delete(
            user=user,
            book_id=request_serializer.book_id
        )
    except FavoriteMapperException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=SuccessResponseSerializer(result=result).data)
