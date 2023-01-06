from rest_framework.serializers import ModelSerializer
from books_service.models import Genre, Author, Book


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self._data = {}
    
    def to_representation(self, instance: Book) -> dict:
        self._data.update({
            "id": instance.id,
            "name": instance.name,
            "image_id": instance.image_id,
            "price": instance.price,
            "amount": instance.amount,
            "genre": GenreSerializer(instance=instance.genre).data,
            "author": AuthorSerializer(instance=instance.author).data,
            "description": instance.description,
            "created_at": instance.created_at
        })
        return self._data
