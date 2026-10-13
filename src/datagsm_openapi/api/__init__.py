"""API modules for DataGSM OpenAPI SDK."""

from .club import ClubApi, ClubRequest, ClubWriteRequest
from .neis import MealRequest, NeisApi, ScheduleRequest, TimetableRequest
from .project import ProjectApi, ProjectRequest
from .student import CreateStudentRequest, StudentApi, StudentRequest, UpdateStudentRequest

__all__ = [
    "ClubApi",
    "ClubRequest",
    "ClubWriteRequest",
    "CreateStudentRequest",
    "MealRequest",
    "NeisApi",
    "ProjectApi",
    "ProjectRequest",
    "ScheduleRequest",
    "StudentApi",
    "StudentRequest",
    "TimetableRequest",
    "UpdateStudentRequest",
]
