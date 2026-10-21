"""Exception classes for DataGSM OpenAPI SDK."""

from typing import Any, Optional


class DataGsmException(Exception):
    """Base exception for all DataGSM API errors.

    Attributes:
        message: Human-readable error message
        status_code: HTTP status code if available
        response_body: Raw response body if available
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code
            response_body: Raw response body
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        """Return string representation of the exception."""
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message

    def __repr__(self) -> str:
        """Return detailed representation of the exception."""
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"status_code={self.status_code!r})"
        )


class BadRequestException(DataGsmException):
    """Exception raised for 400 Bad Request errors.

    Indicates that the request was malformed or contained invalid parameters.
    """

    def __init__(
        self,
        message: str = "Bad request",
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            response_body: Raw response body
        """
        super().__init__(message=message, status_code=400, response_body=response_body)


class UnauthorizedException(DataGsmException):
    """Exception raised for 401 Unauthorized errors.

    Indicates that the API key is missing or invalid.
    """

    def __init__(
        self,
        message: str = "Unauthorized: Invalid or missing API key",
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            response_body: Raw response body
        """
        super().__init__(message=message, status_code=401, response_body=response_body)


class ForbiddenException(DataGsmException):
    """Exception raised for 403 Forbidden errors.

    Indicates that the API key doesn't have permission for the requested resource.
    """

    def __init__(
        self,
        message: str = "Forbidden: Insufficient permissions",
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            response_body: Raw response body
        """
        super().__init__(message=message, status_code=403, response_body=response_body)


class NotFoundException(DataGsmException):
    """Exception raised for 404 Not Found errors.

    Indicates that the requested resource was not found.
    """

    def __init__(
        self,
        message: str = "Not found",
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            response_body: Raw response body
        """
        super().__init__(message=message, status_code=404, response_body=response_body)


class ConflictException(DataGsmException):
    """Exception raised for 409 Conflict errors.

    Indicates that the request conflicts with existing data, such as a duplicate
    email, student number, club name, or project name.
    """

    def __init__(
        self,
        message: str = "Conflict",
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            response_body: Raw response body
        """
        super().__init__(message=message, status_code=409, response_body=response_body)


class RateLimitException(DataGsmException):
    """Exception raised for 429 Too Many Requests errors.

    Indicates that the rate limit has been exceeded.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            response_body: Raw response body
        """
        super().__init__(message=message, status_code=429, response_body=response_body)


class ServerErrorException(DataGsmException):
    """Exception raised for 5xx Server Error responses.

    Indicates that the server encountered an error processing the request.
    """

    def __init__(
        self,
        message: str = "Internal server error",
        status_code: int = 500,
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code (5xx)
            response_body: Raw response body
        """
        super().__init__(
            message=message,
            status_code=status_code,
            response_body=response_body,
        )


class NetworkException(DataGsmException):
    """Exception raised for network-related errors.

    Indicates connection failures, timeouts, or other network issues.
    """

    def __init__(
        self,
        message: str,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            original_exception: The underlying exception that caused this error
        """
        super().__init__(message=message)
        self.original_exception = original_exception


class ValidationException(DataGsmException):
    """Exception raised for data validation errors.

    Indicates that response data failed validation against the expected schema.
    """

    def __init__(
        self,
        message: str,
        validation_errors: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            validation_errors: List of validation errors from Pydantic
        """
        super().__init__(message=message)
        self.validation_errors = validation_errors or []
