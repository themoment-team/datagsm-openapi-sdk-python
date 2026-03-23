"""Club API module for DataGSM OpenAPI SDK."""

from dataclasses import dataclass
from typing import Optional

from ..models import ClubDetail, ClubResponse, ClubSortBy, ClubStatus, ClubType, SortDirection
from ._base import BaseApi


@dataclass
class ClubRequest:
    """동아리 조회 요청 파라미터 (Club Query Parameters).

    Attributes:
        club_id: Club ID for exact match
        club_name: Club name for filtering
        club_type: Club type filter (MAJOR_CLUB, AUTONOMOUS_CLUB)
        status: Club operation status filter (ACTIVE, ABOLISHED)
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
            "status": self.status.value if self.status else None,
            "page": self.page,
            "size": self.size,
            "includeLeaderInParticipants": self.include_leader_in_participants,
            "sortBy": self.sort_by.value if self.sort_by else None,
            "sortDirection": self.sort_direction.value,
        }
        return params


class ClubApi(BaseApi):
    """동아리 데이터 API (Club Data API).

    Provides methods for querying club information.
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
