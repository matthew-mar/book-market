class UsersServiceException(Exception):
    FAILED_GET_USER_MESSAGE = "failed get user"

    FAILED_GET_FAVORITES = "failed get books from favorites"

    @staticmethod
    def failed_get_user():
        raise UsersServiceException(
            args=UsersServiceException.FAILED_GET_USER_MESSAGE
        )
