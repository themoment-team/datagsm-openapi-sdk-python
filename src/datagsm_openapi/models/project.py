"""Project-related models for DataGSM OpenAPI SDK."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .club import Club
from .enums import Major, ProjectStatus, Sex


class ParticipantInfo(BaseModel):
    """동아리 부원/프로젝트 참가자 정보 (Participant Information).

    Information about a club member or project participant.

    Attributes:
        id: Student ID
        name: Student name
        email: Email address
        student_number: Student ID number
        major: Major
        sex: Gender
    """

    id: int = Field(..., description="Student ID")
    name: str = Field(..., description="Student name")
    email: str = Field(..., description="Email address")
    student_number: int = Field(..., alias="studentNumber", description="Student ID number")
    major: Major = Field(..., description="Major")
    sex: Sex = Field(..., description="Gender")

    model_config = ConfigDict(populate_by_name=True)


class Project(BaseModel):
    """프로젝트 정보 (Project Information).

    Information about a project including description and participants.

    Attributes:
        id: Project ID
        name: Project name
        description: Project description
        club: Associated club
        participants: List of project participants
        start_year: Year the project started
        end_year: Year the project ended (None if still active)
        status: Project operation status (ACTIVE or ENDED)
    """

    id: int = Field(..., description="Project ID")
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    club: Optional[Club] = Field(None, description="Associated club")
    participants: list[ParticipantInfo] = Field(
        default_factory=list, description="Project participants"
    )
    start_year: int = Field(..., alias="startYear", description="Year the project started")
    end_year: Optional[int] = Field(
        None, alias="endYear", description="Year the project ended"
    )
    status: ProjectStatus = Field(..., description="Project operation status")

    model_config = ConfigDict(populate_by_name=True)


class ProjectResponse(BaseModel):
    """프로젝트 목록 응답 (Project List Response).

    Response model for paginated project list queries.

    Attributes:
        total_pages: Total number of pages
        total_elements: Total number of projects matching the query
        projects: List of projects
    """

    total_pages: int = Field(..., alias="totalPages", description="Total number of pages")
    total_elements: int = Field(
        ..., alias="totalElements", description="Total number of projects"
    )
    projects: list[Project] = Field(default_factory=list, description="List of projects")

    model_config = ConfigDict(populate_by_name=True)
