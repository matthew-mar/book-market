from orders_service.exceptions.mappers import (
    DeliveryMethodMapperException,
    PayMenthodMapperException,
    BooksetMapperException, 
    OrderMapperException,
    CartMapperException,
)
from orders_service.models import (
    DeliveryMethod, 
    PayMethod, 
    Bookset, 
    Order,
    Cart, 
)

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db.models import QuerySet

from uuid import UUID, uuid4


class PayMethodMapper:
    @staticmethod
    def all() -> QuerySet[PayMethod]:
        return PayMethod.objects.all()
    
    @staticmethod
    def get_by_id(id: UUID) -> PayMethod:
        try:
            return PayMethod.objects.get(id=id)
        except ObjectDoesNotExist:
            raise PayMenthodMapperException(
                PayMenthodMapperException.PAYMENT_METHOD_NOT_EXIST_MESSAGE
            )


class DeliveryMethodMapper:
    @staticmethod
    def all() -> QuerySet[DeliveryMethod]:
        return DeliveryMethod.objects.all()

    @staticmethod
    def get_by_id(id: UUID) -> DeliveryMethod:
        try:
            return DeliveryMethod.objects.get(id=id)
        except ObjectDoesNotExist:
            raise DeliveryMethodMapperException(
                DeliveryMethodMapperException.DELIVERY_METHOD_NOT_EXIST_MESSAGE
            )


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
    def delete_book_from_cart(user_id: UUID, book_id: UUID) -> bool:
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

    @staticmethod
    def delete(user_id: UUID, set_id: UUID) -> bool:
        try:
            Cart.objects.get(user_id=user_id, set_id=set_id).delete()
            return True
        except ObjectDoesNotExist:
            raise CartMapperException(
                CartMapperException.CART_EMPTY_MESSAGE
            )


class OrderMapper:
    @staticmethod
    def create(
        payment_method: PayMethod, 
        delivery_method: DeliveryMethod,
        address: str,
        set_id: UUID,
        user_id: UUID
    ) -> Order:
        try:
            order = Order(
                payment_method=payment_method, 
                delivery_method=delivery_method,
                address=address,
                set_id=set_id,
                user_id=user_id
            )

            order.save()

            try:
                CartMapper.delete(user_id=user_id, set_id=set_id)
            except CartMapperException as e:
                raise OrderMapperException(
                    f"{OrderMapperException.FAILED_CREATE_MESSAGE}: {e.args[0]}"
                )

            return order
        except IntegrityError:
            raise OrderMapperException(
                OrderMapperException.ORDER_ALREADY_EXIST_MESSAGE
            )

    @staticmethod
    def get_for_user_by_id(user_id: UUID, id: UUID) -> Order:
        try:
            return Order.objects.get(user_id=user_id, id=id)
        except ObjectDoesNotExist:
            raise OrderMapperException(
                OrderMapperException.ORDER_NOT_EXIST_MESSAGE
            )

    @staticmethod
    def find_for_user(user_id: UUID) -> QuerySet[Order]:
        return Order.objects.filter(user_id=user_id)
