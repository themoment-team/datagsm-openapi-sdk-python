"""HTTP client abstraction layer for DataGSM OpenAPI SDK."""

from typing import Any, NoReturn, Optional

import httpx

from ._version import __version__
from .exceptions import (
    BadRequestException,
    ConflictException,
    DataGsmException,
    ForbiddenException,
    NetworkException,
    NotFoundException,
    RateLimitException,
    ServerErrorException,
    UnauthorizedException,
    ValidationException,
)

_STATUS_EXCEPTIONS: dict[int, type[DataGsmException]] = {
    400: BadRequestException,
    401: UnauthorizedException,
    403: ForbiddenException,
    404: NotFoundException,
    409: ConflictException,
    429: RateLimitException,
}


class HttpClient:
    """HTTP client wrapper around httpx with error handling.

    This class provides a clean interface for making HTTP requests to the DataGSM API
    with automatic error handling and exception mapping.

    Attributes:
        base_url: Base URL for the API
        api_key: API key for authentication
        timeout: Request timeout in seconds
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the HTTP client.

        Args:
            base_url: Base URL for the API
            api_key: API key for authentication
            timeout: Request timeout in seconds (default: 30.0)
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._client: Optional[httpx.Client] = None

    def __enter__(self) -> "HttpClient":
        """Enter context manager."""
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self._get_headers(),
        )
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit context manager and close the client."""
        self.close()

    def _get_headers(self) -> dict[str, str]:
        """Get common headers for all requests.

        Returns:
            Dictionary of HTTP headers
        """
        return {
            "X-API-KEY": self.api_key,
            "Accept": "application/json",
            "User-Agent": f"datagsm-openapi-sdk-python/{__version__}",
        }

    def _get_client(self) -> httpx.Client:
        """Get or create the HTTP client.

        Returns:
            The httpx.Client instance
        """
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self._get_headers(),
            )
        return self._client

    def _handle_error(self, response: httpx.Response) -> NoReturn:
        """Handle HTTP error responses.

        Args:
            response: The HTTP response object

        Raises:
            BadRequestException: For 400 errors
            UnauthorizedException: For 401 errors
            ForbiddenException: For 403 errors
            NotFoundException: For 404 errors
            ConflictException: For 409 errors
            RateLimitException: For 429 errors
            ServerErrorException: For 5xx errors
            DataGsmException: For other errors
        """
        error_body: Optional[dict[str, Any]] = None
        error_message = response.text or f"HTTP {response.status_code} error"
        try:
            parsed = response.json()
        except ValueError:
            parsed = None
        if isinstance(parsed, dict):
            error_body = parsed
            message = parsed.get("message")
            if isinstance(message, str) and message:
                error_message = message

        status_code = response.status_code
        exception_type = _STATUS_EXCEPTIONS.get(status_code)

        if exception_type is not None:
            raise exception_type(message=error_message, response_body=error_body)
        if 500 <= status_code < 600:
            raise ServerErrorException(
                message=error_message,
                status_code=status_code,
                response_body=error_body,
            )
        raise DataGsmException(
            message=error_message,
            status_code=status_code,
            response_body=error_body,
        )

    def request(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[Any] = None,
    ) -> Optional[Any]:
        """Send an HTTP request and decode the JSON response body.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path (e.g., "/v1/students")
            params: Query parameters
            json: JSON request body

        Returns:
            Decoded JSON body, or None when the response has no body (e.g. 204 No Content)

        Raises:
            NetworkException: For connection or timeout errors
            ValidationException: If a non-empty success body is not valid JSON
            DataGsmException: For API errors
        """
        try:
            client = self._get_client()
            response = client.request(method, path, params=params, json=json)
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            raise NetworkException(
                message=f"Network error: {e!s}",
                original_exception=e,
            ) from e
        except httpx.HTTPError as e:
            raise NetworkException(
                message=f"HTTP error: {e!s}",
                original_exception=e,
            ) from e

        if response.is_error:
            self._handle_error(response)

        if response.status_code == 204 or not response.content.strip():
            return None
        try:
            return response.json()
        except ValueError as e:
            raise ValidationException(
                message=f"Response body is not valid JSON (HTTP {response.status_code})",
            ) from e

    def get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
    ) -> Optional[Any]:
        """Make a GET request. See :meth:`request`."""
        return self.request("GET", path, params=params)

    def post(
        self,
        path: str,
        json: Optional[Any] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Optional[Any]:
        """Make a POST request. See :meth:`request`."""
        return self.request("POST", path, params=params, json=json)

    def put(
        self,
        path: str,
        json: Optional[Any] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Optional[Any]:
        """Make a PUT request. See :meth:`request`."""
        return self.request("PUT", path, params=params, json=json)

    def delete(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
    ) -> Optional[Any]:
        """Make a DELETE request. See :meth:`request`."""
        return self.request("DELETE", path, params=params)

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._client is not None:
            self._client.close()
            self._client = None
