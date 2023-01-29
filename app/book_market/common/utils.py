from dataclasses import dataclass
from random import randint
from typing import Any
from uuid import UUID


def is_valid_uuid(value: Any) -> bool:
    if isinstance(value, UUID):
        return True
    try:
        UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def big_int() -> int:
    return randint(1_000_000, 9_999_999)


@dataclass
class HttpMethod:
    GET = "GET"

    POST = "POST"

    DELETE = "DELETE"

    PATCH = "PATCH"
