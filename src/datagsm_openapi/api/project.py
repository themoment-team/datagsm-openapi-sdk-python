"""Project API module for DataGSM OpenAPI SDK."""

from dataclasses import dataclass
from typing import Optional

from ..models import Project, ProjectResponse, ProjectSortBy, ProjectStatus, SortDirection
from ._base import BaseApi


@dataclass
class ProjectRequest:
    """프로젝트 조회 요청 파라미터 (Project Query Parameters).

    Attributes:
        project_id: Project ID for exact match
        project_name: Project name for filtering
        club_id: Club ID filter
        status: Project operation status filter (default: ACTIVE)
        page: Page number (default: 0)
        size: Page size (default: 100)
        sort_by: Sort field
        sort_direction: Sort direction (default: ASC)
    """

    project_id: Optional[int] = None
    project_name: Optional[str] = None
    club_id: Optional[int] = None
    status: Optional[ProjectStatus] = ProjectStatus.ACTIVE
    page: int = 0
    size: int = 100
    sort_by: Optional[ProjectSortBy] = None
    sort_direction: SortDirection = SortDirection.ASC

    def to_params(self) -> dict[str, Optional[object]]:
        """Convert to query parameters dictionary.

        Returns:
            Dictionary of query parameters
        """
        params: dict[str, Optional[object]] = {
            "projectId": self.project_id,
            "projectName": self.project_name,
            "clubId": self.club_id,
            "status": self.status.value if self.status else None,
            "page": self.page,
            "size": self.size,
            "sortBy": self.sort_by.value if self.sort_by else None,
            "sortDirection": self.sort_direction.value,
        }
        return params


class ProjectApi(BaseApi):
    """프로젝트 데이터 API (Project Data API).

    Provides methods for querying project information.
    """

    def get_projects(self, request: Optional[ProjectRequest] = None) -> ProjectResponse:
        """프로젝트 목록 조회 (Get Project List).

        Query projects with optional filtering, sorting, and pagination.

        Args:
            request: Query parameters (optional)

        Returns:
            Paginated project response

        Example:
            >>> api = ProjectApi(http_client)
            >>> # Get all projects
            >>> response = api.get_projects()
            >>> print(f"Total: {response.total_elements}")
            >>>
            >>> # Filter by club
            >>> request = ProjectRequest(club_id=1)
            >>> club_projects = api.get_projects(request)
        """
        req = request or ProjectRequest()
        return self._get("/v1/projects", params=req.to_params(), response_type=ProjectResponse)

    def get_project(self, project_id: int) -> Optional[Project]:
        """특정 프로젝트 조회 (Get Specific Project).

        Retrieve a single project by ID.

        Args:
            project_id: Project ID

        Returns:
            Project information if found, None otherwise

        Example:
            >>> api = ProjectApi(http_client)
            >>> project = api.get_project(1)
            >>> if project:
            ...     print(f"Project: {project.name}")
            ...     print(f"Description: {project.description}")
        """
        request = ProjectRequest(project_id=project_id)
        response = self.get_projects(request)

        if response.projects:
            return response.projects[0]
        return None
