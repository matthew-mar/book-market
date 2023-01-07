from dataclasses import dataclass
from typing import Self
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
