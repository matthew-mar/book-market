from users_service.views.internal.favorite.mutations import (
    favorites_controller
)
from django.urls import path

urlpatterns = [
    path(route="internal/favorites", view=favorites_controller),
]
