class BooksetMapperException(Exception):
    SET_NOT_EXISTS_MESSAGE = "set not exist"

    BOOK_ALREARY_IN_SET_MESSAGE = "book already in set"


class CartMapperException(Exception):
    BOOK_ALREADY_IN_CART_MESSAGE = "book already in cart"
