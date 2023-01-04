from orders_service.views.public.delivery_method.details import (
    get_delivery_methods
)
from django.urls import path

urlpatterns = [
    path(route="delivery-methods", view=get_delivery_methods),
]
