from books_service.models import Genre
from django.db.models import QuerySet


class GenreMapper:
    @staticmethod
    def all() -> QuerySet[Genre]:
        return Genre.objects.all()
