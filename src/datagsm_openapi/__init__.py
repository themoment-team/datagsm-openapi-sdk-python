"""DataGSM OpenAPI SDK for Python.

Official Python SDK for the DataGSM OpenAPI service.

Example:
    Basic usage::

        from datagsm_openapi import DataGsmClient

        with DataGsmClient(api_key="your-api-key") as client:
            students = client.students.get_students()
            print(f"Total students: {students.total_elements}")
"""

from .api import (
    ClubApi,
    ClubRequest,
    MealRequest,
    NeisApi,
    ProjectApi,
    ProjectRequest,
    ScheduleRequest,
    StudentApi,
    StudentRequest,
)
from .client import DataGsmClient
from .exceptions import (
    BadRequestException,
    DataGsmException,
    ForbiddenException,
    NetworkException,
    NotFoundException,
    RateLimitException,
    ServerErrorException,
    UnauthorizedException,
    ValidationException,
)

__version__ = "1.0.3"

__all__ = [
    "BadRequestException",
    "ClubApi",
    "ClubRequest",
    "DataGsmClient",
    "DataGsmException",
    "ForbiddenException",
    "MealRequest",
    "NeisApi",
    "NetworkException",
    "NotFoundException",
    "ProjectApi",
    "ProjectRequest",
    "RateLimitException",
    "ScheduleRequest",
    "ServerErrorException",
    "StudentApi",
    "StudentRequest",
    "UnauthorizedException",
    "ValidationException",
]
