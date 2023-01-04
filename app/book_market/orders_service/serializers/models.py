from rest_framework.serializers import ModelSerializer
from orders_service.models import PayMethod, DeliveryMethod


class PayMethodSerializer(ModelSerializer):
    class Meta:
        model = PayMethod
        fields = "__all__"


class DeliveryMethodSerializer(ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = "__all__"
