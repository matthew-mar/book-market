from books_service.models import Book
from django.db.models import QuerySet
from dataclasses import dataclass

from common.dto import BookSetPaginatedList


@dataclass
class BooksFromBookset:
    books: QuerySet[Book]
    paginated_booksets: BookSetPaginatedList
