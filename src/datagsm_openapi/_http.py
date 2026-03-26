"""HTTP client abstraction layer for DataGSM OpenAPI SDK."""

from typing import Any, Optional

import httpx

from . import __version__
from .exceptions import (
    BadRequestException,
    DataGsmException,
    ForbiddenException,
    NetworkException,
    NotFoundException,
    RateLimitException,
    ServerErrorException,
    UnauthorizedException,
)


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

    def _handle_error(self, response: httpx.Response) -> None:
        """Handle HTTP error responses.

        Args:
            response: The HTTP response object

        Raises:
            BadRequestException: For 400 errors
            UnauthorizedException: For 401 errors
            ForbiddenException: For 403 errors
            NotFoundException: For 404 errors
            RateLimitException: For 429 errors
            ServerErrorException: For 5xx errors
            DataGsmException: For other errors
        """
        try:
            error_body = response.json()
            error_message = error_body.get("message", response.text)
        except Exception:
            error_body = None
            error_message = response.text or f"HTTP {response.status_code} error"

        status_code = response.status_code

        if status_code == 400:
            raise BadRequestException(message=error_message, response_body=error_body)
        elif status_code == 401:
            raise UnauthorizedException(message=error_message, response_body=error_body)
        elif status_code == 403:
            raise ForbiddenException(message=error_message, response_body=error_body)
        elif status_code == 404:
            raise NotFoundException(message=error_message, response_body=error_body)
        elif status_code == 429:
            raise RateLimitException(message=error_message, response_body=error_body)
        elif 500 <= status_code < 600:
            raise ServerErrorException(
                message=error_message,
                status_code=status_code,
                response_body=error_body,
            )
        else:
            raise DataGsmException(
                message=error_message,
                status_code=status_code,
                response_body=error_body,
            )

    def get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make a GET request.

        Args:
            path: API endpoint path (e.g., "/students")
            params: Query parameters

        Returns:
            JSON response as a dictionary

        Raises:
            NetworkException: For connection or timeout errors
            DataGsmException: For API errors
        """
        try:
            client = self._get_client()
            response = client.get(path, params=params)
            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]
        except httpx.HTTPStatusError as e:
            self._handle_error(e.response)
            raise  # This line will never be reached, but makes mypy happy
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

    def post(
        self,
        path: str,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make a POST request.

        Args:
            path: API endpoint path
            json: JSON request body
            params: Query parameters

        Returns:
            JSON response as a dictionary

        Raises:
            NetworkException: For connection or timeout errors
            DataGsmException: For API errors
        """
        try:
            client = self._get_client()
            response = client.post(path, json=json, params=params)
            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]
        except httpx.HTTPStatusError as e:
            self._handle_error(e.response)
            raise
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

    def put(
        self,
        path: str,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make a PUT request.

        Args:
            path: API endpoint path
            json: JSON request body
            params: Query parameters

        Returns:
            JSON response as a dictionary

        Raises:
            NetworkException: For connection or timeout errors
            DataGsmException: For API errors
        """
        try:
            client = self._get_client()
            response = client.put(path, json=json, params=params)
            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]
        except httpx.HTTPStatusError as e:
            self._handle_error(e.response)
            raise
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

    def delete(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make a DELETE request.

        Args:
            path: API endpoint path
            params: Query parameters

        Returns:
            JSON response as a dictionary

        Raises:
            NetworkException: For connection or timeout errors
            DataGsmException: For API errors
        """
        try:
            client = self._get_client()
            response = client.delete(path, params=params)
            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]
        except httpx.HTTPStatusError as e:
            self._handle_error(e.response)
            raise
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

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._client is not None:
            self._client.close()
            self._client = None
