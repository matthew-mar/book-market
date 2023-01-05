class BooksetMapperException(Exception):
    SET_NOT_EXISTS_MESSAGE = "set not exist"

    BOOK_ALREARY_IN_SET_MESSAGE = "book already in set"

    BOOK_NOT_EXIST_MESSAGE = "book not exist in set"


class CartMapperException(Exception):
    BOOK_ALREADY_IN_CART_MESSAGE = "book already in cart"

    BOOK_NOT_EXIST_IN_CART_MESSAGE = "book not exist in cart"

    CART_EMPTY_MESSAGE = "cart is empty"
