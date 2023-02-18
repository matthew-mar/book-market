from dataclasses import dataclass
from typing import Any, Self
from uuid import UUID

from common.utils import is_valid_uuid


@dataclass
class UserData:
    _id: UUID
    name: str
    surname: str
    email: str
    phone_number: str | None
    token: str | None


@dataclass
class FavoritesList:
    books: list[UUID]
    count: int
    next_page: int
    previous_page: int
    page_size: int


@dataclass
class BooksetData:
    _id: UUID
    set_id: UUID
    user_id: UUID
    book_id: UUID
    amount: int


@dataclass
class BooksetDataList:
    count: int
    next_page: int
    previous_page: int
    page_size: int
    bookset_list: list[BooksetData]


@dataclass
class PaginatedResponse:
    count: int
    next_page: int
    previous_page: int
    page_size: int
    results: list[Any]

    @property
    def json(self: Self) -> dict:
        return {
            "count": self.count,
            "next_page": self.next_page,
            "previous_page": self.previous_page,
            "page_size": self.page_size,
            "results": self.results,
        }


@dataclass
class BookSetMap:
    book_id: UUID
    amount: int

    @property
    def json(self: Self) -> dict:
        return {
            str(self.book_id): {
                "amount": self.amount
            }
        }
    
    @staticmethod
    def from_json(data: dict) -> Self:
        try:
            book_id = list(data.keys())[0]

            if not is_valid_uuid(value=book_id):
                raise Exception(
                    "failed convert to bookset map: book_id must be a valid "
                    "UUID string"
                )

            amount = data[book_id]["amount"]

            if not isinstance(amount, int):
                raise Exception(
                    "failed convert to bookset map: amount must be an integer"
                )

            return BookSetMap(book_id=book_id, amount=amount)
        
        except IndexError:
            raise Exception(
                "failed convert to bookset map: no book_id in dict"
            )
        
        except KeyError:
            raise Exception(
                "failet convert to bookset map: no key named amount"
            )


@dataclass
class BookSetPaginatedList:
    count: int
    next_page: int
    previous_page: int
    page_size: int
    bookset_list: list[BookSetMap]

    @property
    def book_ids(self: Self) -> list[UUID]:
        return list(map(lambda bookset: bookset.book_id, self.bookset_list))
    
    @property
    def booksets(self: Self) -> dict:
        booksets = {}

        for bookset in self.bookset_list:
            booksets.update(bookset.json)
        
        return booksets
