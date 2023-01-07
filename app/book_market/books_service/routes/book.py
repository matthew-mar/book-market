from books_service.views.public.book.mutations import add_to_favorites
from books_service.views.public.book.details import (
    favorites,
    paginate, 
    bookset,
    detail, 
)
from django.urls import path

urlpatterns = [
    path(route="<uuid:book_id>", view=detail),
    path(route="", view=paginate),
    path(route="favorites", view=favorites),
    path(route="bookset", view=bookset),
    path(route="<uuid:book_id>/favorite", view=add_to_favorites),
]
