from orders_service.models import PayMethod
from django.db.models import QuerySet


class PayMethodMapper:
    @staticmethod
    def all() -> QuerySet:
        return PayMethod.objects.all()
