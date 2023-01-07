from dataclasses import dataclass
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
