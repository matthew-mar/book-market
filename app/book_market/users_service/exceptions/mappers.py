class FavoriteMapperException(Exception):
    ALREADY_EXISTS_MESSAGE = "book already in favorites"

    @staticmethod
    def already_exists():
        raise FavoriteMapperException(
            FavoriteMapperException.ALREADY_EXISTS_MESSAGE
        )
