from orders_service.views.internal.cart.mutations import add_to_cart
from django.urls import path

urlpatterns = [
    path(route="internal/cart", view=add_to_cart),
]
