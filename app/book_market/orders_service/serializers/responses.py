from orders_service.serializers.models import BooksetSerializer
from common.serializers.responses import PaginatedResponseSerializer
from rest_framework.pagination import DjangoPaginator
from typing import Self


class BooksInBooksetPaginatedResponseSerializer(PaginatedResponseSerializer):
    def __init__(
        self: Self, 
        paginator: DjangoPaginator, 
        page_number: int
    ) -> Self:
        super().__init__(paginator, page_number)
        self.results = BooksetSerializer(
            instance=self.page.object_list,
            many=True
        ).data
