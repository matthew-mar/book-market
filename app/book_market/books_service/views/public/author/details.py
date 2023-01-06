from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from books_service.serializers.models import AuthorSerializer
from books_service.mappers import AuthorMapper


@api_view(http_method_names=["GET"])
def authors(request: Request) -> Response:
    authors = AuthorMapper.all()

    response_serializer = AuthorSerializer(instance=authors, many=True)

    return Response(data=response_serializer.data)
