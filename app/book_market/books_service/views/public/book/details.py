from books_service.exceptions.mappers import BookMapperException
from books_service.serializers.responses import (
    PaginatedBookListResponseSerializer,
    BookDetailResponseSerializer,
    FavoriteResponseSerializer,
    BooksetResponseSerializer,
)
from books_service.serializers.requests import (
    PaginatedSetRequestSerializer,
    BooksFilterRequestSerializer,
)
from books_service.dto import BooksFromBookset
from books_service.mappers import BookMapper
from books_service.models import Book

from common.dto import PaginatedResponse
from common.services import UsersService, OrdersService
from common.middlewares import view_wrapper
from common.serializers.requests import (
    PaginationRequestSerializer, 
    BaseRequestSerializer,
)
from common.exceptions.internal import (
    OrdersServiceException,
    UsersServiceException,
)
from common.exceptions.service import (
    BadRequestException,
    NotFoundException,
)
from common.utils import HttpMethod

from rest_framework.permissions import IsAuthenticated
from django.db.models import QuerySet
from uuid import UUID


@view_wrapper(
    http_method_names=[HttpMethod.GET],
    response_serializer_class=BookDetailResponseSerializer
)
def detail(request_serializer: BaseRequestSerializer, book_id: UUID) -> Book:
    try:
        return BookMapper.get_by_id(id=book_id)
    except BookMapperException as e:
        raise NotFoundException(detail=e.args[0])


@view_wrapper(
    http_method_names=[HttpMethod.GET],
    request_serializer_class=BooksFilterRequestSerializer,
    response_serializer_class=PaginatedBookListResponseSerializer
)
def paginate(
    request_serializer: BooksFilterRequestSerializer
) -> QuerySet[Book]:
    return BookMapper.filter_books(
        filter_param="created_at",  # TODO: filter param from request
        filter_order=request_serializer.order
    )


@view_wrapper(
    http_method_names=[HttpMethod.GET],
    request_serializer_class=PaginationRequestSerializer,
    response_serializer_class=FavoriteResponseSerializer,
    permissions=[IsAuthenticated]
)
def favorites(
    request_serializer: PaginationRequestSerializer
) -> PaginatedResponse:
    try:
        favorites_response = UsersService.get_from_favorites(
            jwt_token=request_serializer.user.token,
            page=request_serializer.page,
            page_size=request_serializer.page_size
        )
    except UsersServiceException as e:
        raise BadRequestException(detail=e.args[0])
    
    books = BookMapper.find_by_ids(ids=favorites_response.books)
    if len(books) != len(favorites_response.books):
        raise BadRequestException(detail="failed get books from favorites")

    return PaginatedResponse(
        count=favorites_response.count,
        next_page=favorites_response.next,
        previous_page=favorites_response.previous,
        page_size=favorites_response.page_size,
        results=books
    )


@view_wrapper(
    http_method_names=[HttpMethod.GET],
    request_serializer_class=PaginatedSetRequestSerializer,
    response_serializer_class=BooksetResponseSerializer,
    permissions=[IsAuthenticated]
)
def bookset(
    request_serializer: PaginatedSetRequestSerializer
) -> BooksFromBookset:
    try:
        paginated_bookset = OrdersService.get_from_bookset(
            jwt_token=request_serializer.user.token,
            set_id=request_serializer.set_id,
            page=request_serializer.page,
            page_size=request_serializer.page_size
        )
    except OrdersServiceException as e:
        raise BadRequestException(detail=e.args[0])
    
    books = BookMapper.find_by_ids(ids=paginated_bookset.book_ids)

    return BooksFromBookset(books=books, paginated_booksets=paginated_bookset)
