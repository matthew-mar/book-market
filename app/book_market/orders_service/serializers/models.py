from orders_service.models import PayMethod, DeliveryMethod, Bookset, Order
from rest_framework.serializers import ModelSerializer

from common.dto import BookSetMap


class PayMethodSerializer(ModelSerializer):
    class Meta:
        model = PayMethod
        fields = "__all__"


class DeliveryMethodSerializer(ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = "__all__"


class BooksetSerializer(ModelSerializer):
    class Meta:
        model = Bookset
        fields = "__all__"


class BooksetInPaginationListSerializer(BooksetSerializer):
    def to_representation(self, instance: Bookset):
        return BookSetMap(
            book_id=instance.book_id, 
            amount=instance.amount
        ).json


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user_id", "number", "address", "set_id", "created_at")
