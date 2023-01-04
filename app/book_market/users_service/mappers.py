from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from users_service.exceptions.mappers import FavoriteMapperException
from users_service.models import Favorite, User

from uuid import UUID


class UserMapper:
    @staticmethod
    def get_by_id(id: UUID) -> User | None:
        try:
            return User.objects.get(id=id)
        except ObjectDoesNotExist:
            return None


class FavoriteMapper:
    @staticmethod
    def create(user: User, book_id: UUID) -> bool:
        try:
            Favorite(user=user, book_id=book_id).save()
            return True
        except IntegrityError:
            FavoriteMapperException.already_exists()

    @staticmethod
    def delete(user: User, book_id: UUID) -> bool:
        try:
            Favorite.objects.get(user=user, book_id=book_id).delete()
            return True
        except ObjectDoesNotExist:
            FavoriteMapperException.non_exist()
