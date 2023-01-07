from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from books_service.exceptions.mappers import BookMapperException
from books_service.models import Genre, Author, Book

from uuid import UUID


class GenreMapper:
    @staticmethod
    def all() -> QuerySet[Genre]:
        return Genre.objects.all()


class AuthorMapper:
    @staticmethod
    def all() -> QuerySet[Author]:
        return Author.objects.all()


class BookMapper:
    @staticmethod
    def get_by_id(id: UUID) -> Book:
        try:
            return Book.objects.get(id=id)
        except ObjectDoesNotExist:
            raise BookMapperException(
                BookMapperException.BOOK_NOT_EXIST_MESSAGE
            )

    @staticmethod
    def filter_books(filter_param: str, filter_order: str) -> QuerySet[Book]:
        return Book.objects.all().order_by(f"{filter_order}{filter_param}")
    
    @staticmethod
    def find_by_ids(ids: list[UUID]) -> QuerySet[Book]:
        return Book.objects.filter(id__in=ids)

    @staticmethod
    def decrease_book_amount(book: Book) -> bool:
        if book.amount == 1:
            book.delete()
        
        book.amount -= 1
        book.save()

        return True
