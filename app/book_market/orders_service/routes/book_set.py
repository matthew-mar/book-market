from orders_service.views.internal.book_set.details import paginate_bookset
from django.urls import path

urlpatterns = [
    path(route="internal/book-set/<uuid:set_id>", view=paginate_bookset),
]
