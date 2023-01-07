from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from common.serializers.responses import SuccessResponseSerializer
from common.serializers.requests import ForBookRequestSerializer
from common.exceptions.service import BadRequestException
from common.exceptions.internal import UsersServiceException
from common.services import UsersService

from orders_service.exceptions.mappers import CartMapperException
from orders_service.mappers import CartMapper


@api_view(http_method_names=["POST"])
@permission_classes(permission_classes=[IsAuthenticated])
def increase(request: Request) -> Response:
    request_serializer = ForBookRequestSerializer(requrest=request)

    try:
        user = UsersService.me(jwt_token=request.headers.get("Authorization"))
    except UsersServiceException as e:
        raise BadRequestException(detail=e.args[0])
    
    try:
        result = CartMapper.increase_book_amount(
            user_id=user.id, 
            book_id=request_serializer.book_id
        )
    except CartMapperException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=SuccessResponseSerializer(result=result).data)


@api_view(http_method_names=["POST"])
@permission_classes(permission_classes=[IsAuthenticated])
def decrease(request: Request) -> Response:
    request_serializer = ForBookRequestSerializer(requrest=request)

    try:
        user = UsersService.me(jwt_token=request.headers.get("Authorization"))
    except UsersServiceException as e:
        raise BadRequestException(detail=e.args[0])
    
    try:
        result = CartMapper.decrease_book_amount(
            user_id=user.id,
            book_id=request_serializer.book_id
        )
    except CartMapperException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=SuccessResponseSerializer(result=result).data)
