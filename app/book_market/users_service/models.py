from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from users_service.managers import CustomUserManager
from uuid import uuid4


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    name = models.TextField(max_length=255, null=False)
    surname = models.TextField(max_length=255, null=False)
    phone_number = models.TextField(max_length=12, unique=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = CustomUserManager()
