from books_service.views.public.genre.details import genres
from django.urls import path

urlpatterns = [
    path(route="genres", view=genres),
]
