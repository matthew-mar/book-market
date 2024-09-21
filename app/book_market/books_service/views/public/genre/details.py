from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from books_service.serializers.models import GenreSerializer
from books_service.mappers import GenreMapper


@api_view(http_method_names=["GET"])
def genres(request: Request) -> Response:
    genres = GenreMapper.all()

    response_serializer = GenreSerializer(instance=genres, many=True)

    return Response(data=response_serializer.data)
