"""Student API module for DataGSM OpenAPI SDK."""

from dataclasses import dataclass
from typing import Any, Optional

from .._json import enum_value
from ..models import Major, Sex, SortDirection, Student, StudentResponse, StudentRole, StudentSortBy
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
        specialty: Specialty filter (e.g. Backend)
        major: Major (department) filter
        github_id: GitHub ID filter (partial match)
        include_graduates: Include graduated students (server default: False)
        include_withdrawn: Include withdrawn students (server default: False)
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
    specialty: Optional[str] = None
    major: Optional[Major] = None
    github_id: Optional[str] = None
    include_graduates: Optional[bool] = None
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
            "specialty": self.specialty,
            "major": self.major.value if self.major else None,
            "githubId": self.github_id,
            "includeGraduates": self.include_graduates,
            "includeWithdrawn": self.include_withdrawn,
            "onlyEnrolled": self.only_enrolled,
            "page": self.page,
            "size": self.size,
            "sortBy": self.sort_by.value if self.sort_by else None,
            "sortDirection": self.sort_direction.value,
        }
        return params


@dataclass
class CreateStudentRequest:
    """학생 생성 요청 본문 (Create Student Request Body).

    Mirrors the server's ``CreateStudentReqDto``. Enrolled students
    (GENERAL_STUDENT, STUDENT_COUNCIL, DORMITORY_MANAGER) require grade, class_num and
    number. GRADUATE students cannot have a student number, dormitory room or clubs, and
    WITHDRAWN students cannot have a dormitory room or clubs.

    Attributes:
        name: Student name (max 30 characters)
        sex: Gender
        email: Email address (max 50 characters)
        grade: Grade (1-3, required for enrolled students)
        class_num: Class number (1-4, required for enrolled students)
        number: Student number within class (1-18, required for enrolled students)
        role: Student role (default: GENERAL_STUDENT)
        dormitory_room_number: Dormitory room number (201-518)
        major_club_id: Major club ID
        autonomous_club_id: Autonomous club ID
        specialty: Specialty (max 50 characters, e.g. 백엔드)
    """

    name: str
    sex: Sex
    email: str
    grade: Optional[int] = None
    class_num: Optional[int] = None
    number: Optional[int] = None
    role: StudentRole = StudentRole.GENERAL_STUDENT
    dormitory_room_number: Optional[int] = None
    major_club_id: Optional[int] = None
    autonomous_club_id: Optional[int] = None
    specialty: Optional[str] = None

    def to_body(self) -> dict[str, Any]:
        """Convert to the JSON request body.

        Returns:
            Dictionary of request body fields
        """
        return {
            "name": self.name,
            "sex": enum_value(self.sex),
            "email": self.email,
            "grade": self.grade,
            "classNum": self.class_num,
            "number": self.number,
            "role": enum_value(self.role),
            "dormitoryRoomNumber": self.dormitory_room_number,
            "majorClubId": self.major_club_id,
            "autonomousClubId": self.autonomous_club_id,
            "specialty": self.specialty,
        }


@dataclass
class UpdateStudentRequest:
    """학생 수정 요청 본문 (Update Student Request Body).

    Mirrors the server's ``UpdateStudentReqDto``. The update replaces the whole student
    record, so optional fields left as None are cleared on the server. The major is
    derived from ``class_num``. Graduated or withdrawn students cannot be updated, and
    ``role`` cannot be changed to GRADUATE or WITHDRAWN through this API.

    Attributes:
        name: Student name (max 30 characters)
        sex: Gender
        email: Email address (max 50 characters)
        grade: Grade (1-3)
        class_num: Class number (1-4)
        number: Student number within class (1-18)
        role: Student role
        dormitory_room_number: Dormitory room number (201-518)
        major_club_id: Major club ID
        autonomous_club_id: Autonomous club ID
        specialty: Specialty (max 50 characters)
        github_id: GitHub account ID (max 39 characters)
    """

    name: str
    sex: Sex
    email: str
    grade: int
    class_num: int
    number: int
    role: StudentRole
    dormitory_room_number: Optional[int] = None
    major_club_id: Optional[int] = None
    autonomous_club_id: Optional[int] = None
    specialty: Optional[str] = None
    github_id: Optional[str] = None

    def to_body(self) -> dict[str, Any]:
        """Convert to the JSON request body.

        Returns:
            Dictionary of request body fields
        """
        return {
            "name": self.name,
            "sex": enum_value(self.sex),
            "email": self.email,
            "grade": self.grade,
            "classNum": self.class_num,
            "number": self.number,
            "role": enum_value(self.role),
            "dormitoryRoomNumber": self.dormitory_room_number,
            "majorClubId": self.major_club_id,
            "autonomousClubId": self.autonomous_club_id,
            "specialty": self.specialty,
            "githubId": self.github_id,
        }


class StudentApi(BaseApi):
    """학생 데이터 API (Student Data API).

    Provides methods for querying, creating, and updating student information.
    Write methods require an API key with the STUDENT_WRITE scope.
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

        Retrieve a single student by ID, including graduated and withdrawn students.

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
        request = StudentRequest(
            student_id=student_id, include_graduates=True, include_withdrawn=True
        )
        response = self.get_students(request)

        if response.students:
            return response.students[0]
        return None

    def create_student(self, request: CreateStudentRequest) -> Student:
        """학생 생성 (Create Student).

        Args:
            request: Student data to create

        Returns:
            The created student

        Raises:
            BadRequestException: If validation fails (e.g. missing student number)
            NotFoundException: If a referenced club does not exist
            ConflictException: If the email or student number already exists

        Example:
            >>> student = api.create_student(
            ...     CreateStudentRequest(
            ...         name="홍길동", sex=Sex.MAN, email="s24001@gsm.hs.kr",
            ...         grade=1, class_num=1, number=1,
            ...     )
            ... )
        """
        return self._send("POST", "/v1/students", Student, body=request.to_body())

    def update_student(self, student_id: int, request: UpdateStudentRequest) -> Student:
        """학생 정보 수정 (Update Student).

        Replaces the student's information with the given values.

        Args:
            student_id: Student ID
            request: New student data

        Returns:
            The updated student

        Raises:
            BadRequestException: If validation fails, or the student is a graduate or
                withdrawn student
            NotFoundException: If the student or a referenced club does not exist
            ConflictException: If the email or student number is already used
        """
        return self._send(
            "PUT", f"/v1/students/{student_id}", Student, body=request.to_body()
        )
