"""Club-related models for DataGSM OpenAPI SDK."""

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

from .enums import ClubStatus, ClubType

if TYPE_CHECKING:
    from .project import ParticipantInfo


class Club(BaseModel):
    """동아리 정보 - 간단 버전 (Club Information - Simple Version).

    Basic club information used in references from other models.

    Attributes:
        id: Club ID
        name: Club name
        type: Club type (MAJOR_CLUB, JOB_CLUB, AUTONOMOUS_CLUB)
    """

    id: int = Field(..., description="Club ID")
    name: str = Field(..., description="Club name")
    type: ClubType = Field(..., description="Club type")

    model_config = ConfigDict(populate_by_name=True)


class ClubDetail(BaseModel):
    """동아리 상세 정보 (Club Detail Information).

    Detailed club information including leader and member list.

    Attributes:
        id: Club ID
        name: Club name
        type: Club type
        status: Club operation status (ACTIVE or ABOLISHED)
        founded_year: Year the club was founded
        abolished_year: Year the club was abolished (None if still active)
        leader: Club leader information
        participants: List of club members
    """

    id: int = Field(..., description="Club ID")
    name: str = Field(..., description="Club name")
    type: ClubType = Field(..., description="Club type")
    status: Optional[ClubStatus] = Field(None, description="Club operation status")
    founded_year: Optional[int] = Field(
        None, alias="foundedYear", description="Year the club was founded"
    )
    abolished_year: Optional[int] = Field(
        None, alias="abolishedYear", description="Year the club was abolished"
    )
    leader: "ParticipantInfo" = Field(..., description="Club leader")
    participants: list["ParticipantInfo"] = Field(
        default_factory=list, description="Club members"
    )

    model_config = ConfigDict(populate_by_name=True)


class ClubResponse(BaseModel):
    """동아리 목록 응답 (Club List Response).

    Response model for paginated club list queries.

    Attributes:
        total_pages: Total number of pages
        total_elements: Total number of clubs matching the query
        clubs: List of clubs with details
    """

    total_pages: int = Field(..., alias="totalPages", description="Total number of pages")
    total_elements: int = Field(..., alias="totalElements", description="Total number of clubs")
    clubs: list[ClubDetail] = Field(default_factory=list, description="List of clubs")

    model_config = ConfigDict(populate_by_name=True)


# Resolve forward references for ClubDetail
from .project import ParticipantInfo  # noqa: E402

ClubDetail.model_rebuild()
