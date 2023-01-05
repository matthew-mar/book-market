from orders_service.views.internal.cart.mutations import cart_controller
from django.urls import path

urlpatterns = [
    path(route="internal/cart", view=cart_controller),
]
