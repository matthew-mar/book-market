from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from common.serializers.responses import SuccessResponseSerializer
from common.serializers.requests import ForBookRequestSerializer
from common.exceptions.service import BadRequestException
from common.exceptions.internal import DjoserException
from common.services import DjoserService

from orders_service.exceptions.mappers import CartMapperException
from orders_service.mappers import CartMapper


@api_view(http_method_names=["POST", "DELETE"])
@permission_classes(permission_classes=[IsAuthenticated])
def cart_controller(request: Request) -> Response:
    match (request.method):
        case "POST":
            return add_to_cart(request=request)
        case "DELETE":
            return delete_from_cart(request=request)


def add_to_cart(request: Request) -> Response:
    request_serializer = ForBookRequestSerializer(requrest=request)

    try:
        user = DjoserService.me(jwt_token=request.headers.get("Authorization"))
    except DjoserException as e:
        raise BadRequestException(detail=e.args[0])
    
    try:
        result = CartMapper.add_or_create(
            user_id=user.id, 
            book_id=request_serializer.book_id
        )
    except CartMapperException as e:
        raise BadRequestException(detail=e.args[0])

    return Response(data=SuccessResponseSerializer(result=result).data)


def delete_from_cart(request: Request) -> Response:
    request_serializer = ForBookRequestSerializer(requrest=request)

    try:
        user = DjoserService.me(jwt_token=request.headers.get("Authorization"))
    except DjoserException as e:
        raise BadRequestException(detail=e.args[0])
    
    try:
        result = CartMapper.delete_book_from_cart(
            user_id=user.id, 
            book_id=request_serializer.book_id
        )
    except CartMapperException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=SuccessResponseSerializer(result=result).data)
