from common.serializers.responses import PaginatedResponseSerializer
from books_service.serializers.models import BookSerializer
from rest_framework.pagination import DjangoPaginator
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
