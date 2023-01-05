from django.urls import path, include

NAMESPACE = "orders_service.routes"

urlpatterns = [
    path("", include(f"{NAMESPACE}.pay_method")),
    path("", include(f"{NAMESPACE}.delivery_method")),
    path("", include(f"{NAMESPACE}.cart")),
]
