class FavoriteMapperException(Exception):
    ALREADY_EXISTS_MESSAGE = "book already in favorites"

    OBJECT_DOES_NOT_EXISTS_MESSAGE = "favorite object does not exist"

    @staticmethod
    def already_exists():
        raise FavoriteMapperException(
            FavoriteMapperException.ALREADY_EXISTS_MESSAGE
        )

    @staticmethod
    def non_exist():
        raise FavoriteMapperException(
            FavoriteMapperException.OBJECT_DOES_NOT_EXISTS_MESSAGE
        )
