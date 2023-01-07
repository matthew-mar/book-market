from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from books_service.exceptions.mappers import BookMapperException
from books_service.mappers import BookMapper

from common.exceptions.service import NotFoundException, BadRequestException
from common.serializers.responses import SuccessResponseSerializer
from common.exceptions.internal import UsersServiceException
from common.services import UsersService

from uuid import UUID


@api_view(http_method_names=["POST"])
@permission_classes(permission_classes=[IsAuthenticated])
def add_to_favorites(request: Request, book_id: UUID) -> Response:
    try:
        book = BookMapper.get_by_id(id=book_id)

        result = UsersService.add_to_favorites(
            jwt_token=request.headers.get("Authorization"),
            book_id=book.id
        )
    
    except BookMapperException as e:
        raise NotFoundException(detail=e.args[0])
    
    except UsersServiceException as e:
        raise BadRequestException(detail=e.args[0])
    
    return Response(data=SuccessResponseSerializer(result=result).data)
