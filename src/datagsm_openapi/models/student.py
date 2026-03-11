"""Student-related models for DataGSM OpenAPI SDK."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .club import Club
from .enums import Major, Sex, StudentRole


class Student(BaseModel):
    """학생 정보 (Student Information).

    Represents detailed information about a student including their
    personal information, class details, dormitory assignment, and club memberships.

    Attributes:
        id: Student ID
        name: Student name
        sex: Gender
        email: Email address
        grade: Grade (1-3)
        class_num: Class number
        number: Student number within class
        student_number: Full student ID number
        major: Major (SW_DEVELOPMENT, SMART_IOT, AI)
        role: Student role (GENERAL_STUDENT, STUDENT_COUNCIL, WITHDRAWN, etc.)
        dormitory_floor: Dormitory floor number
        dormitory_room: Dormitory room number
        major_club: Major club membership
        autonomous_club: Autonomous club membership
    """

    id: int = Field(..., description="Student ID")
    name: str = Field(..., description="Student name")
    sex: Sex = Field(..., description="Gender")
    email: str = Field(..., description="Email address")
    grade: int = Field(..., ge=1, le=3, description="Grade (1-3)")
    class_num: int = Field(..., alias="classNum", description="Class number")
    number: int = Field(..., description="Student number within class")
    student_number: int = Field(..., alias="studentNumber", description="Full student ID number")
    major: Major = Field(..., description="Major")
    role: StudentRole = Field(..., description="Student role")
    dormitory_floor: Optional[int] = Field(
        None, alias="dormitoryFloor", description="Dormitory floor"
    )
    dormitory_room: Optional[int] = Field(
        None, alias="dormitoryRoom", description="Dormitory room"
    )
    major_club: Optional[Club] = Field(None, alias="majorClub", description="Major club")
    autonomous_club: Optional[Club] = Field(
        None, alias="autonomousClub", description="Autonomous club"
    )

    model_config = ConfigDict(populate_by_name=True)


class StudentResponse(BaseModel):
    """학생 목록 응답 (Student List Response).

    Response model for paginated student list queries.

    Attributes:
        students: List of students
        total_elements: Total number of students matching the query
        total_pages: Total number of pages
    """

    students: list[Student] = Field(default_factory=list, description="List of students")
    total_elements: int = Field(..., alias="totalElements", description="Total number of students")
    total_pages: int = Field(..., alias="totalPages", description="Total number of pages")

    model_config = ConfigDict(populate_by_name=True)
