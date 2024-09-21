from django.contrib.admin import ModelAdmin, register
from orders_service.models import (
    DeliveryMethod,
    PayMethod,
    Bookset,
    Order,
    Cart,
)


@register(DeliveryMethod)
class DeliveryMethodAdmin(ModelAdmin):
    pass


@register(PayMethod)
class PayMethodAdmin(ModelAdmin):
    pass


@register(Bookset)
class BooksetAdmin(ModelAdmin):
    pass


@register(Order)
class OrderAdmin(ModelAdmin):
    pass


@register(Cart)
class CarAdmin(ModelAdmin):
    pass
