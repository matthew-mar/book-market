from common.utils import big_int
from django.db import models
from uuid import uuid4


class PayMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(max_length=30, null=False, unique=True)


class DeliveryMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(max_length=30, null=False, unique=True)


class Bookset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    set_id = models.UUIDField(null=False)
    user_id = models.UUIDField(null=False)
    book_id = models.UUIDField(null=False)
    amount = models.IntegerField(default=1)

    class Meta:
        unique_together = ("set_id", "user_id", "book_id")


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.UUIDField(null=False, unique=True)
    set_id = models.UUIDField(null=False, unique=True)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.UUIDField(null=False)
    number = models.BigIntegerField(null=False, unique=True, default=big_int)
    delivery_method = models.ForeignKey(
        null=True,
        to=DeliveryMethod, 
        on_delete=models.SET_NULL
    )
    payment_method = models.ForeignKey(
        null=True,
        to=PayMethod,
        on_delete=models.SET_NULL
    )
    address = models.TextField(max_length=50, null=False)
    set_id = models.UUIDField(null=False, unique=True)
    created_at = models.DateTimeField(null=False, auto_now=True)
