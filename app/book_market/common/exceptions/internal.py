class DjoserException(Exception):
    FAILED_GET_USER_MESSAGE = "failed get user"

    @staticmethod
    def failed_get_user():
        raise DjoserException(args=DjoserException.FAILED_GET_USER_MESSAGE)
