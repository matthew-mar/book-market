from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request

from common.serializers.responses import BaseResponseSerializer
from common.serializers.requests import BaseRequestSerializer

from typing import Callable


# TODO: подумать еще над названиями
def view_wrapper(
    http_method_names: list[str],
    response_serializer_class: BaseResponseSerializer,
    request_serializer_class: BaseRequestSerializer = BaseRequestSerializer,
    permissions: list[type] = []
) -> Callable:
    def middleware(view: Callable) -> Callable:
        
        @api_view(http_method_names=http_method_names)
        @permission_classes(permission_classes=permissions)
        def wrapper(request: Request, **kwargs) -> Response:
            request_serializer = request_serializer_class(
                request=request,
                **kwargs
            )

            response_serializer = response_serializer_class(
                request_serializer=request_serializer,
                result=view(request_serializer, **kwargs)
            )

            return Response(data=response_serializer.data)

        return wrapper
    
    return middleware
