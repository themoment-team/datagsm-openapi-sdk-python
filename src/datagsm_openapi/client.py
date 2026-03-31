"""Main client class for DataGSM OpenAPI SDK."""

from typing import Any, Optional

from ._http import HttpClient
from .api import ClubApi, NeisApi, ProjectApi, StudentApi


class DataGsmClient:
    """Main client for interacting with the DataGSM OpenAPI.

    This is the main entry point for the SDK. Create an instance with your API key
    and use it to access various API endpoints.

    Example:
        Basic usage::

            with DataGsmClient(api_key="your-api-key") as client:
                students = client.students.get_students()

    Attributes:
        base_url: Base URL for the API
        timeout: Request timeout in seconds
    """

    DEFAULT_BASE_URL = "https://openapi.datagsm.kr"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the DataGSM client.

        Args:
            api_key: Your DataGSM API key
            base_url: Base URL for the API (default: https://openapi.datagsm.kr)
            timeout: Request timeout in seconds (default: 30.0)
        """
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout
        self._http_client = HttpClient(
            base_url=self.base_url,
            api_key=api_key,
            timeout=timeout,
        )

        # Initialize API modules
        self._student_api = StudentApi(self._http_client)
        self._club_api = ClubApi(self._http_client)
        self._project_api = ProjectApi(self._http_client)
        self._neis_api = NeisApi(self._http_client)

    @property
    def students(self) -> StudentApi:
        """Access the Student API.

        Returns:
            StudentApi instance

        Example:
            >>> with DataGsmClient(api_key="key") as client:
            ...     students = client.students.get_students()
        """
        return self._student_api

    @property
    def clubs(self) -> ClubApi:
        """Access the Club API.

        Returns:
            ClubApi instance

        Example:
            >>> with DataGsmClient(api_key="key") as client:
            ...     clubs = client.clubs.get_clubs()
        """
        return self._club_api

    @property
    def projects(self) -> ProjectApi:
        """Access the Project API.

        Returns:
            ProjectApi instance

        Example:
            >>> with DataGsmClient(api_key="key") as client:
            ...     projects = client.projects.get_projects()
        """
        return self._project_api

    @property
    def neis(self) -> NeisApi:
        """Access the NEIS API.

        Returns:
            NeisApi instance

        Example:
            >>> with DataGsmClient(api_key="key") as client:
            ...     meals = client.neis.get_meals()
        """
        return self._neis_api

    def __enter__(self) -> "DataGsmClient":
        """Enter context manager."""
        self._http_client.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit context manager and close resources."""
        self._http_client.__exit__(*args)

    def close(self) -> None:
        """Close the client and release resources."""
        self._http_client.close()
