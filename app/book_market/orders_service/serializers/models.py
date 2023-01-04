from rest_framework.serializers import ModelSerializer
from orders_service.models import PayMethod


class PayMethodSerializer(ModelSerializer):
    class Meta:
        model = PayMethod
        fields = "__all__"
