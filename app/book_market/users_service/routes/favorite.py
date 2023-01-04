from django.urls import path
from users_service.views.internal.favorite.mutations import add_to_favorites

urlpatterns = [
    path(route="internal/favorites", view=add_to_favorites),
]
