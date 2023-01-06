from orders_service.views.public.order.mutations import create
from django.urls import path

urlpatterns = [
    path(route="", view=create),
]
