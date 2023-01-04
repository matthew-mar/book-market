from orders_service.models import PayMethod, DeliveryMethod
from django.db.models import QuerySet


class PayMethodMapper:
    @staticmethod
    def all() -> QuerySet:
        return PayMethod.objects.all()


class DeliveryMethodMapper:
    @staticmethod
    def all() -> QuerySet:
        return DeliveryMethod.objects.all()
