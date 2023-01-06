from django.contrib.admin import ModelAdmin, register
from books_service.models import Book, Genre, Author


@register(Genre)
class GenreAdmin(ModelAdmin):
    pass


@register(Author)
class AuthorAdmin(ModelAdmin):
    pass


@register(Book)
class BookAdmin(ModelAdmin):
    pass
