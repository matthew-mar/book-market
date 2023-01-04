from typing import Any
from uuid import UUID


def is_valid_uuid(object: Any) -> bool:
    if isinstance(object, UUID):
        return True
    try:
        UUID(object)
        return True
    except (ValueError, AttributeError):
        return False
