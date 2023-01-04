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
