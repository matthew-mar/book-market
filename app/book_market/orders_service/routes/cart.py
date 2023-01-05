from orders_service.views.internal.cart.mutations import cart_controller
from orders_service.views.public.cart.mutations import increase

from django.urls import path

urlpatterns = [
    # internal
    path(route="internal/cart", view=cart_controller),

    # public
    path(route="cart/increase", view=increase),
]
