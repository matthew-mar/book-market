from django.db.models import QuerySet
from typing import Self

from common.serializers.requests import BaseRequestSerializer
from common.serializers.responses import (
    PaginatedResponseSerializer, 
    BaseResponseSerializer,
)
from common.dto import PaginatedResponse

from books_service.serializers.models import AuthorSerializer, BookSerializer
from books_service.serializers.requests import BooksFilterRequestSerializer
from books_service.dto import BooksFromBookset
from books_service.models import Author, Book


class AuthorsReponseSerializer(BaseResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: BaseRequestSerializer, 
        result: QuerySet[Author]
    ) -> Self:
        super().__init__(request_serializer, result)

        self.result = AuthorSerializer(instance=result, many=True).data


class BookDetailResponseSerializer(BaseResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: BaseRequestSerializer, 
        result: Book
    ) -> Self:
        super().__init__(request_serializer, result)

        self.result = BookSerializer(instance=result).data


class PaginatedBookListResponseSerializer(PaginatedResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: BooksFilterRequestSerializer, 
        result: QuerySet[Book]
    ) -> Self:
        super().__init__(request_serializer, result)

        self.result = BookSerializer(instance=result, many=True).data


class FavoriteResponseSerializer(BaseResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: BaseRequestSerializer,
        result: PaginatedResponse
    ) -> Self:
        super().__init__(request_serializer, result)

        result.results = BookSerializer(
            instance=result.results, 
            many=True
        ).data

        self.result = result.json


class BooksetResponseSerializer(BaseResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: BaseRequestSerializer, 
        result: BooksFromBookset
    ) -> Self:
        super().__init__(request_serializer, result)

        books_data = BookSerializer(instance=result.books, many=True).data

        for book in books_data:
            book_id = str(book.get("id"))
            amount_in_bookset = result.paginated_booksets.booksets.get(book_id)
            book["amount"] = amount_in_bookset
        
        self.result = PaginatedResponse(
            count=result.paginated_booksets.count,
            next_page=result.paginated_booksets.next_page,
            previous_page=result.paginated_booksets.previous_page,
            page_size=result.paginated_booksets.page_size,
            results=books_data
        ).json
