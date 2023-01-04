from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users_service.managers import CustomUserManager
from uuid import uuid4


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    name = models.TextField(max_length=255, null=False)
    surname = models.TextField(max_length=255, null=False)
    phone_number = models.TextField(max_length=12, unique=True, null=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = CustomUserManager()


class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book_id = models.UUIDField(null=False)

    class Meta:
        unique_together = ('user', 'book_id')
