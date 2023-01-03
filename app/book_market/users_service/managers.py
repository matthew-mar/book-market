from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str, name: str, surname: str):
        email = self.normalize_email(email=email)
        user = self.model(
            email=email,
            name=name, 
            surname=surname
        )
        user.set_password(password)
        user.save()
        return user
