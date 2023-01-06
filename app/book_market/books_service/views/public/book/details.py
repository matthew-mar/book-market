from rest_framework.pagination import DjangoPaginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from books_service.serializers.requests import BooksFilterRequestSerializer
from books_service.exceptions.mappers import BookMapperException
from books_service.serializers.models import BookSerializer
from books_service.serializers.responses import (
    PaginatedBookListResponseSerializer
)
from books_service.mappers import BookMapper
from books_service.models import Book

from common.exceptions.service import NotFoundException, ValidationException

from uuid import UUID


@api_view(http_method_names=["GET"])
def detail(request: Request, book_id: UUID) -> Response:
    try:
        book = BookMapper.get_by_id(id=book_id)
    except BookMapperException as e:
        raise NotFoundException(detail=e.args[0])
    
    response_serializer = BookSerializer(instance=book)

    return Response(data=response_serializer.data)


@api_view(http_method_names=["GET"])
def paginate(request: Request) -> Response:
    request_serializer = BooksFilterRequestSerializer(request=request)

    books = BookMapper.filter_books(
        filter_param="created_at", 
        filter_order=request_serializer.order
    )

    paginator = DjangoPaginator(
        object_list=books, 
        per_page=request_serializer.page_size
    )

    if paginator.num_pages < request_serializer.page:
        raise ValidationException(
            detail=f"page too large max - {paginator.num_pages}"
        )
    
    response_serializer = PaginatedBookListResponseSerializer(
        paginator=paginator,
        page_number=request_serializer.page
    )

    return Response(data=response_serializer.data)
