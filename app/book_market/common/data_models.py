from dataclasses import dataclass
from typing import Any, Self
from uuid import UUID


@dataclass
class UserData:
    id: UUID
    name: str
    surname: str
    email: str
    phone_number: str | None


@dataclass
class FavoritesList:
    books: list[UUID]
    count: int
    next: int
    previous: int
    page_size: int


@dataclass
class BooksetData:
    id: UUID
    set_id: UUID
    user_id: UUID
    book_id: UUID
    amount: int


@dataclass
class BooksetDataList:
    count: int
    next: int
    previous: int
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
