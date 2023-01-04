from users_service.serializers.models import FavoriteInPaginatorSerializer
from common.serializers.responses import PaginatedResponseSerializer
from rest_framework.pagination import DjangoPaginator
from typing import Self


class FavoritePaginatedResponseSerializer(PaginatedResponseSerializer):
    def __init__(
        self: Self, 
        paginator: DjangoPaginator, 
        page_number: int
    ) -> Self:
        super().__init__(paginator=paginator, page_number=page_number)
        self.results = FavoriteInPaginatorSerializer(
            instance=self.page.object_list,
            many=True
        ).data