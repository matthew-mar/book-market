from rest_framework.serializers import ModelSerializer
from users_service.models import Favorite

from typing import Self


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"


class FavoriteInPaginatorSerializer(FavoriteSerializer):
    def to_representation(self: Self, instance: Favorite):
        return instance.book_id
