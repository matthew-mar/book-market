from django.db import models
from uuid import uuid4


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(max_length=30, null=False, unique=True)


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(max_length=30, null=False, unique=True)
    surname = models.TextField(max_length=30, null=False, unique=True)
