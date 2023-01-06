from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from orders_service.serializers.requests import OrderCreateRequestSerializer
from orders_service.exceptions.mappers import OrderMapperException
from orders_service.mappers import OrderMapper

from common.serializers.responses import SuccessResponseSerializer
from common.exceptions.service import BadRequestException


@api_view(http_method_names=["POST"])
@permission_classes(permission_classes=[IsAuthenticated])
def create(request: Request) -> Response:
    request_serializer = OrderCreateRequestSerializer(request=request)

    try:
        result = OrderMapper.create(
            payment_method=request_serializer.payment_method,
            delivery_method=request_serializer.delivery_method,
            address=request_serializer.address,
            set_id=request_serializer.set_id,
            user_id=request_serializer.user.id
        )
    except OrderMapperException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=SuccessResponseSerializer(result=result).data)
