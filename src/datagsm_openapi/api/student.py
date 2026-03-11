"""Student API module for DataGSM OpenAPI SDK."""

from dataclasses import dataclass
from typing import Optional

from ..models import Sex, SortDirection, Student, StudentResponse, StudentRole, StudentSortBy
from ._base import BaseApi


@dataclass
class StudentRequest:
    """학생 조회 요청 파라미터 (Student Query Parameters).

    Attributes:
        student_id: Student ID for exact match
        name: Student name for filtering
        email: Email address for filtering
        grade: Grade (1-3)
        class_num: Class number
        number: Student number within class
        sex: Gender filter
        role: Student role filter
        dormitory_room: Dormitory room number
        include_withdrawn: Include withdrawn students (default: False)
        only_enrolled: Filter to enrolled students only, excluding GRADUATE and WITHDRAWN
        page: Page number (default: 0)
        size: Page size (default: 300)
        sort_by: Sort field
        sort_direction: Sort direction (default: ASC)
    """

    student_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    grade: Optional[int] = None
    class_num: Optional[int] = None
    number: Optional[int] = None
    sex: Optional[Sex] = None
    role: Optional[StudentRole] = None
    dormitory_room: Optional[int] = None
    include_withdrawn: Optional[bool] = None
    only_enrolled: Optional[bool] = None
    page: int = 0
    size: int = 300
    sort_by: Optional[StudentSortBy] = None
    sort_direction: SortDirection = SortDirection.ASC

    def to_params(self) -> dict[str, Optional[object]]:
        """Convert to query parameters dictionary.

        Returns:
            Dictionary of query parameters
        """
        params: dict[str, Optional[object]] = {
            "studentId": self.student_id,
            "name": self.name,
            "email": self.email,
            "grade": self.grade,
            "classNum": self.class_num,
            "number": self.number,
            "sex": self.sex.value if self.sex else None,
            "role": self.role.value if self.role else None,
            "dormitoryRoom": self.dormitory_room,
            "includeWithdrawn": self.include_withdrawn,
            "onlyEnrolled": self.only_enrolled,
            "page": self.page,
            "size": self.size,
            "sortBy": self.sort_by.value if self.sort_by else None,
            "sortDirection": self.sort_direction.value,
        }
        return params


class StudentApi(BaseApi):
    """학생 데이터 API (Student Data API).

    Provides methods for querying student information.
    """

    def get_students(
        self, request: Optional[StudentRequest] = None
    ) -> StudentResponse:
        """학생 목록 조회 (Get Student List).

        Query students with optional filtering, sorting, and pagination.

        Args:
            request: Query parameters (optional)

        Returns:
            Paginated student response

        Example:
            >>> api = StudentApi(http_client)
            >>> # Get all students
            >>> response = api.get_students()
            >>> print(f"Total: {response.total_elements}")
            >>>
            >>> # Filter by grade
            >>> request = StudentRequest(grade=1)
            >>> first_graders = api.get_students(request)
        """
        req = request or StudentRequest()
        return self._get("/v1/students", params=req.to_params(), response_type=StudentResponse)

    def get_student(self, student_id: int) -> Optional[Student]:
        """특정 학생 조회 (Get Specific Student).

        Retrieve a single student by ID.

        Args:
            student_id: Student ID

        Returns:
            Student information if found, None otherwise

        Example:
            >>> api = StudentApi(http_client)
            >>> student = api.get_student(123)
            >>> if student:
            ...     print(f"Name: {student.name}")
        """
        request = StudentRequest(student_id=student_id)
        response = self.get_students(request)

        if response.students:
            return response.students[0]
        return None
