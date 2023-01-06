from books_service.views.public.book.details import detail, paginate
from django.urls import path

urlpatterns = [
    path(route="<uuid:book_id>", view=detail),
    path(route="", view=paginate),
]
