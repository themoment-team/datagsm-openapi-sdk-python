"""Enum types for DataGSM OpenAPI SDK."""

from enum import Enum


class Sex(str, Enum):
    """성별 (Gender)."""

    MAN = "MAN"
    WOMAN = "WOMAN"


class Major(str, Enum):
    """전공 (Major)."""

    SW_DEVELOPMENT = "SW_DEVELOPMENT"
    SMART_IOT = "SMART_IOT"
    AI = "AI"


class ClubType(str, Enum):
    """동아리 종류 (Club Type)."""

    MAJOR_CLUB = "MAJOR_CLUB"
    AUTONOMOUS_CLUB = "AUTONOMOUS_CLUB"


class StudentRole(str, Enum):
    """학생 역할 (Student Role)."""

    GENERAL_STUDENT = "GENERAL_STUDENT"
    STUDENT_COUNCIL = "STUDENT_COUNCIL"
    DORMITORY_MANAGER = "DORMITORY_MANAGER"
    GRADUATE = "GRADUATE"
    WITHDRAWN = "WITHDRAWN"


class MealType(str, Enum):
    """급식 타입 (Meal Type)."""

    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"


class SortDirection(str, Enum):
    """정렬 방향 (Sort Direction)."""

    ASC = "ASC"  # 오름차순
    DESC = "DESC"  # 내림차순


class StudentSortBy(str, Enum):
    """학생 정렬 기준 (Student Sort By)."""

    ID = "ID"
    NAME = "NAME"
    EMAIL = "EMAIL"
    STUDENT_NUMBER = "STUDENT_NUMBER"
    GRADE = "GRADE"
    CLASS_NUM = "CLASS_NUM"
    NUMBER = "NUMBER"
    MAJOR = "MAJOR"
    ROLE = "ROLE"
    SEX = "SEX"
    DORMITORY_ROOM = "DORMITORY_ROOM"


class ClubSortBy(str, Enum):
    """동아리 정렬 기준 (Club Sort By)."""

    ID = "ID"
    NAME = "NAME"
    TYPE = "TYPE"


class ProjectSortBy(str, Enum):
    """프로젝트 정렬 기준 (Project Sort By)."""

    ID = "ID"
    NAME = "NAME"
