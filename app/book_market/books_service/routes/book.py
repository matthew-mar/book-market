from books_service.views.public.book.details import detail
from django.urls import path

urlpatterns = [
    path(route="<uuid:book_id>", view=detail),
]
