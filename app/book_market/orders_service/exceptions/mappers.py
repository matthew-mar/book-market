class BooksetMapperException(Exception):
    SET_NOT_EXISTS_MESSAGE = "set not exist"

    BOOK_ALREARY_IN_SET_MESSAGE = "book already in set"

    BOOK_NOT_EXIST_MESSAGE = "book not exist in set"


class CartMapperException(Exception):
    BOOK_ALREADY_IN_CART_MESSAGE = "book already in cart"

    BOOK_NOT_EXIST_IN_CART_MESSAGE = "book not exist in cart"

    CART_EMPTY_MESSAGE = "cart is empty"


class OrderMapperException(Exception):
    ORDER_ALREADY_EXIST_MESSAGE = "order already exist"


class PayMenthodMapperException(Exception):
    PAYMENT_METHOD_NOT_EXIST_MESSAGE = "payment method not exist"


class DeliveryMethodMapperException(Exception):
    DELIVERY_METHOD_NOT_EXIST_MESSAGE = "delivery method not exist"
