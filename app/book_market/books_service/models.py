from django.db import models
from uuid import uuid4


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(max_length=30, null=False, unique=True)


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(max_length=30, null=False, unique=True)
    surname = models.TextField(max_length=30, null=False, unique=True)


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(max_length=30, null=False, unique=True)
    image_id = models.TextField(max_length=255, null=True)
    price = models.FloatField(null=False)
    amount = models.IntegerField(default=1)
    genre = models.ForeignKey(
        null=True,
        to=Genre, 
        to_field="id", 
        on_delete=models.SET_NULL
    )
    author = models.ForeignKey(
        null=True,
        to=Author, 
        to_field="id",
        on_delete=models.SET_NULL
    )
    description = models.TextField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now=True)
