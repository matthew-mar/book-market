from common.middlewares import view_wrapper
from common.utils import HttpMethod

from books_service.serializers.responses import AuthorsReponseSerializer
from books_service.mappers import AuthorMapper
from books_service.models import Author

from django.db.models import QuerySet


@view_wrapper(
    http_method_names=[HttpMethod.GET],
    response_serializer_class=AuthorsReponseSerializer
)
def authors(*args) -> QuerySet[Author]:
    return AuthorMapper.all()
