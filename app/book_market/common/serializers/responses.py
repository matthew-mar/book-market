from rest_framework.serializers import BaseSerializer
from rest_framework.pagination import DjangoPaginator

from typing import Self


class SuccessResponseSerializer(BaseSerializer):
    def __init__(self: Self, result: bool):
        self.result = result

    @property
    def data(self: Self):
        return {
            "success": self.result
        }


class PaginatedResponseSerializer(BaseSerializer):
    def __init__(
        self: Self, 
        paginator: DjangoPaginator, 
        page_number: int
    ) -> Self:
        self.page = paginator.get_page(number=page_number)
        self.count = paginator.count
        self.next = (
            None if not self.page.has_next() 
            else self.page.next_page_number()
        )
        self.previous = (
            None if not self.page.has_previous()
            else self.page.previous_page_number()
        )
        self.page_size = paginator.per_page
        self.results = paginator.page_range
    
    @property
    def data(self):
        return {
            "count": self.count,
            "next": self.next,
            "previous": self.previous,
            "page_size": self.page_size,
            "results": self.results,
        }
