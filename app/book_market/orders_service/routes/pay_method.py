from django.urls import path
from orders_service.views.public.pay_method.details import get_payment_methods

urlpatterns = [
    path(route="payment-methods", view=get_payment_methods),
]
