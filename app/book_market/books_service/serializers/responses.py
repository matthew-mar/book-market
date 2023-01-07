from rest_framework.serializers import BaseSerializer
from rest_framework.pagination import DjangoPaginator

from common.data_models import FavoritesList, BooksetDataList, BooksetData
from common.serializers.responses import PaginatedResponseSerializer

from books_service.serializers.models import BookSerializer
from books_service.models import Book

from django.db.models import QuerySet
from typing import Self
from uuid import UUID


class PaginatedBookListResponseSerializer(PaginatedResponseSerializer):
    def __init__(
        self: Self, 
        paginator: DjangoPaginator, 
        page_number: int
    ) -> Self:
        super().__init__(paginator, page_number)
        self.results = BookSerializer(
            instance=self.page.object_list,
            many=True
        ).data


class FavoriteResponseSerializer(BaseSerializer):
    def __init__(
        self: Self, 
        favorites: FavoritesList, 
        books: QuerySet[Book]
    ) -> Self:
        self.favorites = favorites
        self.books = books
    
    @property
    def data(self: Self):
        return {
            "count": self.favorites.count,
            "next": self.favorites.next,
            "previous": self.favorites.previous,
            "page_size": self.favorites.page_size,
            "favorites": BookSerializer(instance=self.books, many=True).data
        }


class BooksetResponseSerializer(BaseSerializer):
    def __init__(
        self: Self,
        bookset_list: BooksetDataList,
        bookset_map: dict[UUID:BooksetData],
        books: QuerySet[Book]
    ) -> Self:
        self.bookset_list = bookset_list
        self.bookset_map = bookset_map
        self.books = books
    
    @property
    def data(self: Self):
        books_serializer_data = BookSerializer(
            instance=self.books, 
            many=True
        ).data

        for book in books_serializer_data:
            book_id = str(book.get("id"))
            amount_in_cart = {
                "amount_in_set": self.bookset_map.get(book_id).amount
            }
            book.update(amount_in_cart)

        return {
            "count": self.bookset_list.count,
            "next": self.bookset_list.next,
            "previous": self.bookset_list.previous,
            "page_size": self.bookset_list.page_size,
            "bookset": books_serializer_data
        }
