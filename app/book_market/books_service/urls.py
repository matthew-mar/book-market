from django.urls import path, include

NAMESPACE = "books_service.routes"

urlpatterns = [
    path("", include(f"{NAMESPACE}.genre")),
    path("", include(f"{NAMESPACE}.author")),
    path("", include(f"{NAMESPACE}.book")),
]
