from common.serializers.responses import PaginatedResponseSerializer
from common.serializers.requests import PaginationRequestSerializer

from users_service.serializers.models import FavoriteInPaginatorSerializer
from users_service.models import Favorite

from django.db.models import QuerySet
from typing import Self


class FavoritePaginatedResponseSerializer(PaginatedResponseSerializer):
    def __init__(
        self: Self, 
        request_serializer: PaginationRequestSerializer, 
        result: QuerySet[Favorite]
    ) -> Self:
        super().__init__(request_serializer, result)

        self.result = FavoriteInPaginatorSerializer(
            instance=result, 
            many=True
        ).data
