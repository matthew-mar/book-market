from orders_service.models import PayMethod, DeliveryMethod, Bookset, Order
from rest_framework.serializers import ModelSerializer


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
        return instance.book_id


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user_id", "number", "address", "set_id", "created_at")
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self._data = {}
    
    def to_representation(self, instance: Order) -> dict:
        self._data.update({
            "id": instance.id,
            "user_id": instance.user_id,
            "number": instance.number,
            "address": instance.address,
            "set_id": instance.set_id,
            "delivery_method": DeliveryMethodSerializer(
                instance=instance.delivery_method
            ).data,
            "payment_method": PayMethodSerializer(
                instance=instance.payment_method
            ).data,
        })
        return self._data
