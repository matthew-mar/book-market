from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from common.exceptions.service import BadRequestException
from common.exceptions.internal import DjoserException
from common.services import DjoserService

from orders_service.serializers.responses import OrderDetailSerializer
from orders_service.exceptions.mappers import OrderMapperException
from orders_service.mappers import OrderMapper

from uuid import UUID


@api_view(http_method_names=["GET"])
@permission_classes(permission_classes=[IsAuthenticated])
def detail(request: Request, order_id: UUID) -> Response:
    try:
        user = DjoserService.me(jwt_token=request.headers.get("Authorization"))
    except DjoserException as e:
        raise BadRequestException(detail=e.args[0])
    
    try:
        order = OrderMapper.get_for_user_by_id(user_id=user.id, id=order_id)
    except OrderMapperException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=OrderDetailSerializer(order=order).data)
