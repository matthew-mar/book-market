from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from books_service.exceptions.mappers import BookMapperException
from books_service.serializers.models import BookSerializer
from books_service.mappers import BookMapper

from common.exceptions.service import NotFoundException
from uuid import UUID


@api_view(http_method_names=["GET"])
def detail(request: Request, book_id: UUID) -> Response:
    try:
        book = BookMapper.get_by_id(id=book_id)
    except BookMapperException as e:
        raise NotFoundException(detail=e.args[0])
    
    response_serializer = BookSerializer(instance=[book], many=True)

    return Response(data=response_serializer.data[0])
