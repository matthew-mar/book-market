from common.serializers.requests import PaginationRequestSerializer
from common.exceptions.internal import DjoserException
from common.services import DjoserService
from common.exceptions.service import (
    ValidationException,
    BadRequestException,
    NotFoundException,
)
from common.utils import is_valid_uuid

from rest_framework.serializers import BaseSerializer
from rest_framework.request import Request

from orders_service.exceptions.mappers import (
    DeliveryMethodMapperException,
    PayMenthodMapperException,
)
from orders_service.mappers import (
    DeliveryMethodMapper,
    PayMethodMapper,
    BooksetMapper, 
)

from typing import Self
from uuid import UUID


class BooksetPaginatedListRequestSerializer(PaginationRequestSerializer):
    def __init__(
        self: Self, 
        request: Request, 
        set_id: UUID, 
        user_id: UUID
    ) -> Self:
        self.user_id = user_id
        self.set_id = set_id
        super().__init__(request)
    
    def validate(self: Self) -> None:
        super().validate()

        books_in_set_count = BooksetMapper.count_for_user_in_set(
            user_id=self.user_id,
            set_id=self.set_id
        )
        if books_in_set_count == 0:
            raise NotFoundException(detail=f"set_id {self.set_id} not exist")


class OrderCreateRequestSerializer(BaseSerializer):
    def __init__(self: Self, request: Request) -> Self:
        self.request = request
        self.validate()

    def validate(self: Self) -> None:
        payment_method_id = self.request.data.get("payment_method_id")
        delivery_method_id = self.request.data.get("delivery_method_id")
        set_id = self.request.data.get("set_id")
        address = self.request.data.get("address")
        
        if payment_method_id is None:
            raise ValidationException(detail="payment_method_id is required")
        
        if not is_valid_uuid(value=payment_method_id):
            raise ValidationException(
                detail=f"payment_method_id value ({payment_method_id}) " 
                    "is not a valid uuid string"
            )

        if delivery_method_id is None:
            raise ValidationException(detail="delivery_method_id is required")
        
        if not is_valid_uuid(value=delivery_method_id):
            raise ValidationException(
                detail=f"delivery_method_id value ({delivery_method_id}) " 
                    "is not a valid uuid string"
            )

        if set_id is None:
            raise ValidationException(detail="set_id is required")
        
        if not is_valid_uuid(value=set_id):
            raise ValidationException(
                detail=f"set_id value ({set_id}) " 
                    "is not a valid uuid string"
            )

        if address is None:
            raise ValidationException(detail="address is required")
        
        if not isinstance(address, str):
            raise ValidationException(detail="address must be string")

        try:
            self.user = DjoserService.me(
                jwt_token=self.request.headers.get("Authorization")
            )
        except DjoserException as e:
            raise BadRequestException(detail=e.args[0])

        try:
            self.payment_method = PayMethodMapper.get_by_id(
                id=payment_method_id
            )
            self.delivery_method = DeliveryMethodMapper.get_by_id(
                id=delivery_method_id
            )

            book_set_count = BooksetMapper.count_for_user_in_set(
                user_id=self.user.id, 
                set_id=set_id
            )
            if book_set_count == 0:
                raise BadRequestException(detail="set does not exist")
            
            self.set_id = set_id
            
        except (DeliveryMethodMapperException, PayMenthodMapperException) as e:
            raise BadRequestException(detail=e.args[0])
        
        self.address = address


class OrderPaginatedListRequestSerializer(PaginationRequestSerializer):
    def __init__(self: Self, request: Request) -> Self:
        super().__init__(request)
    
    def validate(self: Self) -> None:
        super().validate()

        try:
            self.user = DjoserService.me(
                jwt_token=self.request.headers.get("Authorization")
            )
        except DjoserException as e:
            raise BadRequestException(detail=e.args[0])
