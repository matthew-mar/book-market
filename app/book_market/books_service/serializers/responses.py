from rest_framework.serializers import BaseSerializer
from rest_framework.pagination import DjangoPaginator

from common.serializers.responses import PaginatedResponseSerializer
from common.data_models import FavoritesList

from books_service.serializers.models import BookSerializer
from books_service.models import Book

from django.db.models import QuerySet
from typing import Self


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


class FavoriteProductsResponseSerializer(BaseSerializer):
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
