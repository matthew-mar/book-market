from django.contrib.auth.base_user import BaseUserManager
from typing import Self


class CustomUserManager(BaseUserManager):
    def create_user(
        self: Self, 
        email: str, 
        password: str, 
        name: str, 
        surname: str,
        **extra_fields: dict
    ):
        email = self.normalize_email(email=email)
        user = self.model(
            email=email,
            name=name, 
            surname=surname,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self: Self, 
        email: str, 
        password: str, 
        name=None, 
        surname=None
    ):
        return self.create_user(
            email=email,
            password=password,
            name=name,
            surname=surname,
            is_staff=True, 
            is_superuser=True
        )
