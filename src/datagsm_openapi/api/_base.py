"""Base API class for DataGSM OpenAPI SDK."""

from typing import Any, Optional, Type, TypeVar, cast

from pydantic import ValidationError

from .._http import HttpClient
from .._json import clean_params
from ..exceptions import ValidationException
from ..models import CommonApiResponse

T = TypeVar("T")


class BaseApi:
    """Base class for all API modules.

    Provides common functionality for making HTTP requests and parsing responses.
    """

    def __init__(self, http_client: HttpClient) -> None:
        """Initialize the base API.

        Args:
            http_client: HTTP client instance
        """
        self._http = http_client

    def _get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
        response_type: Optional[Type[T]] = None,
    ) -> T:
        """Make a GET request and parse the response.

        Args:
            path: API endpoint path
            params: Query parameters
            response_type: Pydantic model class for response data

        Returns:
            Parsed response data

        Raises:
            ValidationException: If response validation fails
        """
        clean = clean_params(params) if params else None
        response_data = self._http.get(path, params=clean)

        if response_type is None:
            return cast(T, response_data)
        return self._parse_data(response_data, response_type)

    def _send(
        self,
        method: str,
        path: str,
        response_type: Type[T],
        body: Optional[dict[str, Any]] = None,
    ) -> T:
        """Make a write request whose response wraps a data payload.

        Args:
            method: HTTP method
            path: API endpoint path
            response_type: Pydantic model class for response data
            body: JSON request body

        Returns:
            Parsed response data

        Raises:
            ValidationException: If response validation fails
        """
        response_data = self._http.request(method, path, json=body)
        return self._parse_data(response_data, response_type)

    def _send_no_content(
        self,
        method: str,
        path: str,
        body: Optional[dict[str, Any]] = None,
    ) -> None:
        """Make a write request whose endpoint returns no data.

        The server may answer with 204 No Content, an empty 200 body, or a
        ``CommonApiResponse`` envelope without data; all of them are treated as success.

        Args:
            method: HTTP method
            path: API endpoint path
            body: JSON request body
        """
        self._http.request(method, path, json=body)

    @staticmethod
    def _parse_data(response_data: Any, response_type: Type[T]) -> T:
        """Parse a ``CommonApiResponse`` envelope and return its data.

        Args:
            response_data: Decoded JSON response body
            response_type: Pydantic model class for response data

        Returns:
            Parsed response data

        Raises:
            ValidationException: If the body is missing, malformed, or has no data
        """
        if response_data is None:
            raise ValidationException(
                message="Response body is empty",
                validation_errors=[],
            )
        try:
            wrapped_response = CommonApiResponse[response_type].model_validate(  # type: ignore[valid-type]
                response_data
            )
        except ValidationError as e:
            raise ValidationException(
                message=f"Response validation failed: {e!s}",
                validation_errors=cast(list[dict[str, Any]], e.errors()),
            ) from e
        if wrapped_response.data is None:
            raise ValidationException(
                message="Response data is None",
                validation_errors=[],
            )
        return cast(T, wrapped_response.data)
