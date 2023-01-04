from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from orders_service.serializers.models import PayMethodSerializer
from orders_service.mappers import PayMethodMapper


@api_view(http_method_names=["GET"])
def get_payment_methods(request: Request) -> Response:
    payment_methods = PayMethodMapper.all()
    
    response_serializer = PayMethodSerializer(
        instance=payment_methods, 
        many=True
    )

    return Response(data=response_serializer.data)
