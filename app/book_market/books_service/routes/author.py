from books_service.views.public.author.details import authors
from django.urls import path

urlpatterns = [
    path(route="authors", view=authors),
]
