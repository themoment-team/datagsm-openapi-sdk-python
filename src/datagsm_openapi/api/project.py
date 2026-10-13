"""Project API module for DataGSM OpenAPI SDK."""

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Optional, Union

from .._json import enum_value
from ..models import (
    Project,
    ProjectCategory,
    ProjectResponse,
    ProjectSortBy,
    ProjectStatus,
    SortDirection,
)
from ._base import BaseApi


@dataclass
class ProjectRequest:
    """프로젝트 조회 요청 파라미터 (Project Query Parameters).

    Attributes:
        project_id: Project ID for exact match
        project_name: Project name for filtering
        club_id: Club ID filter
        status: Project operation status filter (default: ACTIVE)
        category: Only projects that include this category (default: all)
        page: Page number (default: 0)
        size: Page size (default: 100)
        sort_by: Sort field
        sort_direction: Sort direction (default: ASC)
    """

    project_id: Optional[int] = None
    project_name: Optional[str] = None
    club_id: Optional[int] = None
    status: Optional[ProjectStatus] = ProjectStatus.ACTIVE
    category: Optional[Union[ProjectCategory, str]] = None
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
            "category": enum_value(self.category),
            "page": self.page,
            "size": self.size,
            "sortBy": self.sort_by.value if self.sort_by else None,
            "sortDirection": self.sort_direction.value,
        }
        return params


@dataclass
class ProjectWriteRequest:
    """프로젝트 생성·수정 요청 본문 (Project Create/Update Request Body).

    Mirrors the server's ``ProjectReqDto``.

    ``categories``, ``icon_key`` and ``deployment_url`` distinguish "omit" from "clear":
    leave them as None to omit the field (keeps the current value on update), pass an
    empty list to ``categories`` to remove every category, and pass an empty string to
    ``icon_key`` or ``deployment_url`` to delete the value.

    On update the server keeps the current ``status`` and ``end_year``; use
    :meth:`ProjectApi.end_project` and :meth:`ProjectApi.reactivate_project` to change
    them.

    Attributes:
        name: Project name (max 100 characters)
        description: Project description (max 500 characters)
        start_year: Year the project started
        club_id: Owner club ID (None for no club)
        participant_ids: Participant student IDs
        status: Project operation status (default: ACTIVE, used on create)
        categories: Project categories, multiple allowed (None to omit)
        end_year: Year the project ended (required when creating an ENDED project)
        repositories: Repository URLs (max 20, each max 300 characters)
        tech_stacks: Tech stacks (max 20, each max 50 characters)
        icon_key: Icon object key issued after upload (None to omit, "" to delete)
        deployment_url: Deployment URL starting with http(s):// (None to omit, "" to delete)
    """

    name: str
    description: str
    start_year: int
    club_id: Optional[int] = None
    participant_ids: list[int] = field(default_factory=list)
    status: ProjectStatus = ProjectStatus.ACTIVE
    categories: Optional[Sequence[Union[ProjectCategory, str]]] = None
    end_year: Optional[int] = None
    repositories: list[str] = field(default_factory=list)
    tech_stacks: list[str] = field(default_factory=list)
    icon_key: Optional[str] = None
    deployment_url: Optional[str] = None

    def to_body(self) -> dict[str, Any]:
        """Convert to the JSON request body.

        Returns:
            Dictionary of request body fields. ``categories``, ``iconKey`` and
            ``deploymentUrl`` are only included when they are not None.
        """
        body: dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "startYear": self.start_year,
            "clubId": self.club_id,
            "participantIds": list(self.participant_ids),
            "status": enum_value(self.status),
            "endYear": self.end_year,
            "repositories": list(self.repositories),
            "techStacks": list(self.tech_stacks),
        }
        if isinstance(self.categories, str):
            raise TypeError("categories must be a sequence of categories, not a single string")
        if self.categories is not None:
            body["categories"] = [enum_value(category) for category in self.categories]
        if self.icon_key is not None:
            body["iconKey"] = self.icon_key
        if self.deployment_url is not None:
            body["deploymentUrl"] = self.deployment_url
        return body


@dataclass
class EndProjectRequest:
    """프로젝트 종료 요청 본문 (End Project Request Body).

    Mirrors the server's ``EndProjectReqDto``.

    Attributes:
        end_year: Year the project ended (must not be earlier than the start year)
    """

    end_year: int

    def to_body(self) -> dict[str, Any]:
        """Convert to the JSON request body.

        Returns:
            Dictionary of request body fields
        """
        return {"endYear": self.end_year}


class ProjectApi(BaseApi):
    """프로젝트 데이터 API (Project Data API).

    Provides methods for querying and managing projects.
    Write methods require an API key with the PROJECT_WRITE scope.
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

        Retrieve a single project by ID regardless of its status. The server only returns
        ACTIVE projects unless a status is given, so ENDED projects are looked up as a
        fallback.

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
        for status in (ProjectStatus.ACTIVE, ProjectStatus.ENDED):
            response = self.get_projects(ProjectRequest(project_id=project_id, status=status))
            if response.projects:
                return response.projects[0]
        return None

    def create_project(self, request: ProjectWriteRequest) -> Project:
        """프로젝트 생성 (Create Project).

        Args:
            request: Project data to create

        Returns:
            The created project

        Raises:
            BadRequestException: If validation fails (e.g. ENDED without end_year)
            NotFoundException: If the club or a participant does not exist
            ConflictException: If the project name already exists

        Example:
            >>> project = api.create_project(
            ...     ProjectWriteRequest(
            ...         name="DataGSM", description="학교 데이터 API", start_year=2024,
            ...         club_id=1, participant_ids=[1, 2],
            ...         categories=[ProjectCategory.TEAM, ProjectCategory.CLUB],
            ...     )
            ... )
        """
        return self._send("POST", "/v1/projects", Project, body=request.to_body())

    def update_project(self, project_id: int, request: ProjectWriteRequest) -> Project:
        """프로젝트 정보 수정 (Update Project).

        Replaces the project's information with the given values. Fields documented as
        omittable on :class:`ProjectWriteRequest` keep their current value when None.

        Args:
            project_id: Project ID
            request: New project data

        Returns:
            The updated project

        Raises:
            BadRequestException: If validation fails
            NotFoundException: If the project, club, or a participant does not exist
            ConflictException: If another project already uses the name
        """
        return self._send(
            "PUT", f"/v1/projects/{project_id}", Project, body=request.to_body()
        )

    def delete_project(self, project_id: int) -> None:
        """프로젝트 삭제 (Delete Project).

        Args:
            project_id: Project ID

        Raises:
            NotFoundException: If the project does not exist
        """
        self._send_no_content("DELETE", f"/v1/projects/{project_id}")

    def end_project(self, project_id: int, request: EndProjectRequest) -> None:
        """프로젝트 종료 (End Project).

        Marks an active project as ENDED.

        Args:
            project_id: Project ID
            request: End year information

        Raises:
            BadRequestException: If the end year is earlier than the start year
            NotFoundException: If the project does not exist
        """
        self._send_no_content(
            "POST", f"/v1/projects/{project_id}/end", body=request.to_body()
        )

    def reactivate_project(self, project_id: int) -> None:
        """프로젝트 운영 재개 (Reactivate Project).

        Changes an ENDED project back to ACTIVE.

        Args:
            project_id: Project ID

        Raises:
            NotFoundException: If the project does not exist
        """
        self._send_no_content("POST", f"/v1/projects/{project_id}/reactivate")
