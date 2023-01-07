from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from books_service.exceptions.mappers import BookMapperException
from books_service.mappers import BookMapper

from common.exceptions.service import NotFoundException, BadRequestException
from common.serializers.responses import SuccessResponseSerializer
from common.services import UsersService, OrdersService
from common.exceptions.internal import (
    OrdersServiceException,
    UsersServiceException,
)

from uuid import UUID


@api_view(http_method_names=["POST", "DELETE"])
@permission_classes(permission_classes=[IsAuthenticated])
def favorite_controller(request: Request, book_id: UUID) -> Response:
    match request.method:
        case "POST":
            return add_to_favorites(request=request, book_id=book_id)
        case "DELETE":
            return remove_from_favorites(request=request, book_id=book_id)


@api_view(http_method_names=["POST", "DELETE"])
@permission_classes(permission_classes=[IsAuthenticated])
def cart_controller(request: Request, book_id: UUID) -> Response:
    match request.method:
        case "POST":
            return add_to_cart(request=request, book_id=book_id)
        case "DELETE":
            return remove_from_cart(request=request, book_id=book_id)


def add_to_favorites(request: Request, book_id: UUID) -> Response:
    try:
        book = BookMapper.get_by_id(id=book_id)

        result = UsersService.add_to_favorites(
            jwt_token=request.headers.get("Authorization"),
            book_id=book.id
        )
    
    except BookMapperException as e:
        raise NotFoundException(detail=e.args[0])
    
    except UsersServiceException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=SuccessResponseSerializer(result=result).data)


def remove_from_favorites(request: Request, book_id: UUID) -> Response:
    try:
        book = BookMapper.get_by_id(id=book_id)

        result = UsersService.remove_from_favorites(
            jwt_token=request.headers.get("Authorization"),
            book_id=book.id
        )
    
    except BookMapperException as e:
        raise NotFoundException(detail=e.args[0])
    
    except UsersServiceException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=SuccessResponseSerializer(result=result).data)


def add_to_cart(request: Request, book_id: UUID) -> Response:
    try:
        book = BookMapper.get_by_id(id=book_id)

        result = OrdersService.add_to_cart(
            jwt_token=request.headers.get("Authorization"),
            book_id=book.id
        )
    
    except BookMapperException as e:
        raise NotFoundException(detail=e.args[0])
    
    except OrdersServiceException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=SuccessResponseSerializer(result=result).data)


def remove_from_cart(request: Request, book_id: UUID) -> Response:
    try:
        book = BookMapper.get_by_id(id=book_id)

        result = OrdersService.remove_from_cart(
            jwt_token=request.headers.get("Authorization"),
            book_id=book.id
        )
    
    except BookMapperException as e:
        raise NotFoundException(detail=e.args[0])
    
    except OrdersServiceException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=SuccessResponseSerializer(result=result).data)
