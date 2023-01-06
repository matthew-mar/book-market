from rest_framework.serializers import ModelSerializer
from books_service.models import Genre, Author


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
