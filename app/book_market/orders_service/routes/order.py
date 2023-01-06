from orders_service.views.public.order.details import detail, paginate
from orders_service.views.public.order.mutations import create

from django.urls import path

urlpatterns = [
    path(route="", view=create),
    path(route="<uuid:order_id>", view=detail),
    path(route="list", view=paginate),
]
