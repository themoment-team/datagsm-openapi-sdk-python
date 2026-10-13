"""Club API module for DataGSM OpenAPI SDK."""

from dataclasses import dataclass, field
from typing import Any, Optional

from .._json import enum_value
from ..models import ClubDetail, ClubResponse, ClubSortBy, ClubStatus, ClubType, SortDirection
from ._base import BaseApi


@dataclass
class ClubRequest:
    """동아리 조회 요청 파라미터 (Club Query Parameters).

    Attributes:
        club_id: Club ID for exact match
        club_name: Club name for filtering
        club_type: Club type filter (MAJOR_CLUB, AUTONOMOUS_CLUB)
        status: Club operation status filter (ACTIVE, ABOLISHED), sent as ``clubStatus``
        founded_year: Founded year filter
        page: Page number (default: 0)
        size: Page size (default: 100)
        include_leader_in_participants: Include leader in participants list (default: False)
        sort_by: Sort field
        sort_direction: Sort direction (default: ASC)
    """

    club_id: Optional[int] = None
    club_name: Optional[str] = None
    club_type: Optional[ClubType] = None
    status: Optional[ClubStatus] = None
    founded_year: Optional[int] = None
    page: int = 0
    size: int = 100
    include_leader_in_participants: bool = False
    sort_by: Optional[ClubSortBy] = None
    sort_direction: SortDirection = SortDirection.ASC

    def to_params(self) -> dict[str, Optional[object]]:
        """Convert to query parameters dictionary.

        Returns:
            Dictionary of query parameters
        """
        params: dict[str, Optional[object]] = {
            "clubId": self.club_id,
            "clubName": self.club_name,
            "clubType": self.club_type.value if self.club_type else None,
            "clubStatus": self.status.value if self.status else None,
            "foundedYear": self.founded_year,
            "page": self.page,
            "size": self.size,
            "includeLeaderInParticipants": self.include_leader_in_participants,
            "sortBy": self.sort_by.value if self.sort_by else None,
            "sortDirection": self.sort_direction.value,
        }
        return params


@dataclass
class ClubWriteRequest:
    """동아리 생성·수정 요청 본문 (Club Create/Update Request Body).

    Mirrors the server's ``ClubReqDto``. An ACTIVE club needs a leader or at least one
    participant; an ABOLISHED club must have no leader and no participants.

    Attributes:
        name: Club name (max 30 characters)
        type: Club type (MAJOR_CLUB, AUTONOMOUS_CLUB)
        founded_year: Year the club was founded
        status: Club operation status (ACTIVE, ABOLISHED)
        leader_id: Leader student ID (None for ABOLISHED clubs)
        participant_ids: Member student IDs (max 100, empty for ABOLISHED clubs)
        abolished_year: Year the club was abolished (for ABOLISHED clubs)
    """

    name: str
    type: ClubType
    founded_year: int
    status: ClubStatus
    leader_id: Optional[int] = None
    participant_ids: list[int] = field(default_factory=list)
    abolished_year: Optional[int] = None

    def to_body(self) -> dict[str, Any]:
        """Convert to the JSON request body.

        Returns:
            Dictionary of request body fields
        """
        return {
            "name": self.name,
            "type": enum_value(self.type),
            "leaderId": self.leader_id,
            "participantIds": list(self.participant_ids),
            "foundedYear": self.founded_year,
            "status": enum_value(self.status),
            "abolishedYear": self.abolished_year,
        }


class ClubApi(BaseApi):
    """동아리 데이터 API (Club Data API).

    Provides methods for querying, creating, updating, and deleting clubs.
    Write methods require an API key with the CLUB_WRITE scope.
    """

    def get_clubs(self, request: Optional[ClubRequest] = None) -> ClubResponse:
        """동아리 목록 조회 (Get Club List).

        Query clubs with optional filtering, sorting, and pagination.

        Args:
            request: Query parameters (optional)

        Returns:
            Paginated club response

        Example:
            >>> api = ClubApi(http_client)
            >>> # Get all clubs
            >>> response = api.get_clubs()
            >>> print(f"Total: {response.total_elements}")
            >>>
            >>> # Filter by type
            >>> request = ClubRequest(club_type=ClubType.MAJOR_CLUB)
            >>> major_clubs = api.get_clubs(request)
        """
        req = request or ClubRequest()
        return self._get("/v1/clubs", params=req.to_params(), response_type=ClubResponse)

    def get_club(self, club_id: int) -> Optional[ClubDetail]:
        """특정 동아리 조회 (Get Specific Club).

        Retrieve a single club by ID with detailed information.

        Args:
            club_id: Club ID

        Returns:
            Club detail information if found, None otherwise

        Example:
            >>> api = ClubApi(http_client)
            >>> club = api.get_club(1)
            >>> if club:
            ...     print(f"Club: {club.name}")
            ...     print(f"Leader: {club.leader.name}")
        """
        request = ClubRequest(club_id=club_id)
        response = self.get_clubs(request)

        if response.clubs:
            return response.clubs[0]
        return None

    def create_club(self, request: ClubWriteRequest) -> ClubDetail:
        """동아리 생성 (Create Club).

        Args:
            request: Club data to create

        Returns:
            The created club

        Raises:
            BadRequestException: If validation fails
            NotFoundException: If a referenced student does not exist
            ConflictException: If the club name already exists

        Example:
            >>> club = api.create_club(
            ...     ClubWriteRequest(
            ...         name="SW개발동아리", type=ClubType.MAJOR_CLUB,
            ...         founded_year=2022, status=ClubStatus.ACTIVE,
            ...         leader_id=1, participant_ids=[2, 3],
            ...     )
            ... )
        """
        return self._send("POST", "/v1/clubs", ClubDetail, body=request.to_body())

    def update_club(self, club_id: int, request: ClubWriteRequest) -> ClubDetail:
        """동아리 정보 수정 (Update Club).

        Replaces the club's information with the given values.

        Args:
            club_id: Club ID
            request: New club data

        Returns:
            The updated club

        Raises:
            BadRequestException: If validation fails
            NotFoundException: If the club or a referenced student does not exist
            ConflictException: If another club already uses the name
        """
        return self._send("PUT", f"/v1/clubs/{club_id}", ClubDetail, body=request.to_body())

    def delete_club(self, club_id: int) -> None:
        """동아리 삭제 (Delete Club).

        Args:
            club_id: Club ID

        Raises:
            NotFoundException: If the club does not exist
        """
        self._send_no_content("DELETE", f"/v1/clubs/{club_id}")
