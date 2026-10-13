"""JSON serialization utilities for DataGSM OpenAPI SDK."""

from datetime import date, datetime
from enum import Enum
from typing import Any, Optional, Union


def serialize_date(value: date) -> str:
    """Serialize a date to ISO format string.

    Args:
        value: Date object to serialize

    Returns:
        ISO format date string (YYYY-MM-DD)
    """
    return value.isoformat()


def serialize_datetime(value: datetime) -> str:
    """Serialize a datetime to ISO format string.

    Args:
        value: Datetime object to serialize

    Returns:
        ISO format datetime string
    """
    return value.isoformat()


def enum_value(value: Optional[Union[Enum, str]]) -> Optional[str]:
    """Return the wire value of an enum member, passing plain strings and None through.

    Args:
        value: Enum member, raw string, or None

    Returns:
        The string value to send to the server, or None
    """
    if value is None:
        return None
    if isinstance(value, Enum):
        return str(value.value)
    return value


def clean_params(params: dict[str, Any]) -> dict[str, Any]:
    """Clean query parameters by removing None values and serializing dates.

    Args:
        params: Dictionary of query parameters

    Returns:
        Cleaned dictionary with None values removed and dates serialized
    """
    cleaned: dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, datetime):
            cleaned[key] = serialize_datetime(value)
        elif isinstance(value, date):
            cleaned[key] = serialize_date(value)
        elif isinstance(value, bool):
            # Convert boolean to lowercase string for query params
            cleaned[key] = str(value).lower()
        else:
            cleaned[key] = value
    return cleaned
