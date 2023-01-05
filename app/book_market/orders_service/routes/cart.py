from orders_service.views.public.cart.mutations import increase, decrease
from orders_service.views.internal.cart.mutations import cart_controller

from django.urls import path

urlpatterns = [
    # internal
    path(route="internal/cart", view=cart_controller),

    # public
    path(route="cart/increase", view=increase),
    path(route="cart/decrease", view=decrease),
]
