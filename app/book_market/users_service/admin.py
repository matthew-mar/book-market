from django.contrib.admin import ModelAdmin, register
from users_service.models import Favorite, User


@register(User)
class UserAdmin(ModelAdmin):
    pass


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    pass
