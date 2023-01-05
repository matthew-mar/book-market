from rest_framework.exceptions import APIException, status


class ValidationException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
