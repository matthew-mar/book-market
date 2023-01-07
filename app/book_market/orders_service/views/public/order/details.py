from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import DjangoPaginator
from rest_framework.response import Response
from rest_framework.request import Request

from common.exceptions.service import BadRequestException, ValidationException
from common.exceptions.internal import UsersServiceException
from common.services import UsersService

from orders_service.exceptions.mappers import OrderMapperException
from orders_service.serializers.models import OrderSerializer
from orders_service.serializers.responses import (
    OrderInPaginatedListResponseSerializer,
)
from orders_service.serializers.requests import (
    OrderPaginatedListRequestSerializer
)
from orders_service.mappers import OrderMapper

from uuid import UUID


@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def detail(request: Request, order_id: UUID) -> Response:
    try:
        user = UsersService.me(jwt_token=request.headers.get("Authorization"))
    except UsersServiceException as e:
        raise BadRequestException(detail=e.args[0])
    
    try:
        order = OrderMapper.get_for_user_by_id(user_id=user.id, id=order_id)
    except OrderMapperException as e:
        raise BadRequestException(detail=e.args[0])

    response_serializer = OrderSerializer(
        instance=[order],
        many=True
    )
    
    return Response(data=response_serializer.data[0])


@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def paginate(request: Request) -> Response:
    request_serializer = OrderPaginatedListRequestSerializer(request=request)

    orders = OrderMapper.find_for_user(user_id=request_serializer.user.id)

    paginator = DjangoPaginator(
        object_list=orders, 
        per_page=request_serializer.page_size
    )
    
    if paginator.num_pages < request_serializer.page:
        raise ValidationException(
            detail=f"page number too large max - {paginator.num_pages}"
        )
    
    response_serializer = OrderInPaginatedListResponseSerializer(
        paginator=paginator,
        page_number=request_serializer.page
    )

    return Response(data=response_serializer.data)
