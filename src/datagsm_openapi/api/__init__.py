"""API modules for DataGSM OpenAPI SDK."""

from .club import ClubApi, ClubRequest, ClubWriteRequest
from .neis import MealRequest, NeisApi, ScheduleRequest, TimetableRequest
from .project import EndProjectRequest, ProjectApi, ProjectRequest, ProjectWriteRequest
from .student import CreateStudentRequest, StudentApi, StudentRequest, UpdateStudentRequest

__all__ = [
    "ClubApi",
    "ClubRequest",
    "ClubWriteRequest",
    "CreateStudentRequest",
    "EndProjectRequest",
    "MealRequest",
    "NeisApi",
    "ProjectApi",
    "ProjectRequest",
    "ProjectWriteRequest",
    "ScheduleRequest",
    "StudentApi",
    "StudentRequest",
    "TimetableRequest",
    "UpdateStudentRequest",
]
