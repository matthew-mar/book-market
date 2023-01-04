from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from orders_service.serializers.models import DeliveryMethodSerializer
from orders_service.mappers import DeliveryMethodMapper


@api_view(http_method_names=["GET"])
def get_delivery_methods(request: Request) -> Response:
    delivery_methods = DeliveryMethodMapper.all()

    response_serializer = DeliveryMethodSerializer(
        instance=delivery_methods,
        many=True
    )

    return Response(data=response_serializer.data)
