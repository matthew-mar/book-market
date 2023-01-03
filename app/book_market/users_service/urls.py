from django.urls import path, include

NAMESPACE = "users_service.routes"

urlpatterns = [
    path("", include(f"{NAMESPACE}.djoser")),
]
