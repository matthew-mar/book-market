from orders_service.models import PayMethod, DeliveryMethod, Bookset, Cart
from orders_service.exceptions.mappers import (
    BooksetMapperException, 
    CartMapperException,
)

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db.models import QuerySet

from uuid import UUID, uuid4


class PayMethodMapper:
    @staticmethod
    def all() -> QuerySet:
        return PayMethod.objects.all()


class DeliveryMethodMapper:
    @staticmethod
    def all() -> QuerySet:
        return DeliveryMethod.objects.all()


class BooksetMapper:
    @staticmethod
    def create(user_id: UUID, book_id: UUID) -> Bookset:
        book_set = Bookset(set_id=uuid4(), user_id=user_id, book_id=book_id)
        book_set.save()
        return book_set

    @staticmethod
    def add(user_id: UUID, set_id: UUID, book_id: UUID) -> bool:
        books_in_set = Bookset.objects.filter(user_id=user_id, set_id=set_id)
        
        if len(books_in_set) == 0:
            raise BooksetMapperException(
                BooksetMapperException.SET_NOT_EXISTS_MESSAGE
            )
        
        try:
            Bookset(user_id=user_id, set_id=set_id, book_id=book_id).save()
        except IntegrityError:
            raise BooksetMapperException(
                BooksetMapperException.BOOK_ALREARY_IN_SET_MESSAGE
            )

        return True


class CartMapper:
    @staticmethod
    def add_or_create(user_id: UUID, book_id: UUID) -> bool:
        try:
            cart = Cart.objects.get(user_id=user_id)
            return BooksetMapper.add(
                user_id=user_id, 
                set_id=cart.set_id, 
                book_id=book_id
            )
        except (ObjectDoesNotExist, BooksetMapperException) as e:
            if e.args[0] == BooksetMapperException.BOOK_ALREARY_IN_SET_MESSAGE:
                raise CartMapperException(
                    CartMapperException.BOOK_ALREADY_IN_CART_MESSAGE
                )

            book_set = BooksetMapper.create(user_id=user_id, book_id=book_id)
            Cart(user_id=user_id, set_id=book_set.set_id).save()
        
        return True
