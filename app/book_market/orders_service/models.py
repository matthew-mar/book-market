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
