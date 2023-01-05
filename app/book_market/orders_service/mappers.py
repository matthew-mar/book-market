from orders_service.models import PayMethod, DeliveryMethod, Bookset, Cart
from orders_service.exceptions.mappers import (
    BooksetMapperException, 
    CartMapperException,
)

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db.models import QuerySet

from uuid import UUID, uuid4
import logging


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

    @staticmethod
    def remove(user_id: UUID, set_id: UUID, book_id: UUID) -> bool:
        try:
            Bookset.objects.get(
                user_id=user_id, 
                set_id=set_id, 
                book_id=book_id
            ).delete()
        except ObjectDoesNotExist:
            raise BooksetMapperException(
                BooksetMapperException.BOOK_NOT_EXIST_MESSAGE
            )

        return True

    @staticmethod
    def count_for_user_in_set(user_id: UUID, set_id: UUID) -> int:
        return len(Bookset.objects.filter(user_id=user_id, set_id=set_id))

    
    @staticmethod
    def increase_book_amount(
        user_id: UUID, 
        set_id: UUID, 
        book_id: UUID
    ) -> bool:
        try:
            book_set = Bookset.objects.get(
                user_id=user_id, 
                set_id=set_id, 
                book_id=book_id
            )
            book_set.amount += 1
            book_set.save()

        except ObjectDoesNotExist:
            raise BooksetMapperException(
                BooksetMapperException.BOOK_NOT_EXIST_MESSAGE
            )
        
        return True

    @staticmethod
    def decrease_book_amount(
        user_id: UUID,
        set_id: UUID,
        book_id: UUID
    ) -> bool:
        try:
            book_set = Bookset.objects.get(
                user_id=user_id, 
                set_id=set_id,
                book_id=book_id
            )
            if book_set.amount == 1:
                book_set.delete()
                return True
            
            book_set.amount -= 1
            book_set.save()
            return True
        
        except ObjectDoesNotExist:
            raise BooksetMapperException(
                BooksetMapperException.BOOK_NOT_EXIST_MESSAGE
            )

    @staticmethod
    def find_for_user_in_set(user_id: UUID, set_id: UUID) -> QuerySet[Bookset]:
        return Bookset.objects.filter(user_id=user_id, set_id=set_id)


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

    @staticmethod
    def delete(user_id: UUID, book_id: UUID) -> bool:
        try:
            cart = Cart.objects.get(user_id=user_id)
            
            BooksetMapper.remove(
                user_id=user_id, 
                set_id=cart.set_id, 
                book_id=book_id
            )

            books_in_set_count = BooksetMapper.count_for_user_in_set(
                user_id=user_id, 
                set_id=cart.set_id
            )
            if books_in_set_count == 0:
                cart.delete()
        
        except ObjectDoesNotExist:
            raise CartMapperException(
                CartMapperException.CART_EMPTY_MESSAGE
            )
        
        except BooksetMapperException:
            raise CartMapperException(
                CartMapperException.BOOK_NOT_EXIST_IN_CART_MESSAGE
            )
        
        return True

    @staticmethod
    def increase_book_amount(user_id: UUID, book_id: UUID) -> bool:
        try:
            cart = Cart.objects.get(user_id=user_id)
            return BooksetMapper.increase_book_amount(
                user_id=user_id, 
                set_id=cart.set_id, 
                book_id=book_id
            )
        
        except ObjectDoesNotExist:
            raise CartMapperException(
                CartMapperException.CART_EMPTY_MESSAGE
            )

        except BooksetMapperException:
            raise CartMapperException(
                CartMapperException.BOOK_NOT_EXIST_IN_CART_MESSAGE
            )

    @staticmethod
    def decrease_book_amount(user_id: UUID, book_id: UUID) -> bool:
        try:
            cart = Cart.objects.get(user_id=user_id)
            
            result = BooksetMapper.decrease_book_amount(
                user_id=user_id,
                set_id=cart.set_id,
                book_id=book_id
            )

            books_in_set_amount = BooksetMapper.count_for_user_in_set(
                user_id=user_id, set_id=cart.set_id
            )
            if books_in_set_amount == 0:
                cart.delete()
            
            return result
        
        except ObjectDoesNotExist:
            raise CartMapperException(
                CartMapperException.CART_EMPTY_MESSAGE
            )
        
        except BooksetMapperException:
            raise CartMapperException(
                CartMapperException.BOOK_NOT_EXIST_IN_CART_MESSAGE
            )
