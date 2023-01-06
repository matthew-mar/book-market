from books_service.models import Genre, Author
from django.db.models import QuerySet


class GenreMapper:
    @staticmethod
    def all() -> QuerySet[Genre]:
        return Genre.objects.all()


class AuthorMapper:
    @staticmethod
    def all() -> QuerySet[Author]:
        return Author.objects.all()
