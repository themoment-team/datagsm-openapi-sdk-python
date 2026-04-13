"""API modules for DataGSM OpenAPI SDK."""

from .club import ClubApi, ClubRequest
from .neis import MealRequest, NeisApi, ScheduleRequest, TimetableRequest
from .project import ProjectApi, ProjectRequest
from .student import StudentApi, StudentRequest

__all__ = [
    "ClubApi",
    "ClubRequest",
    "MealRequest",
    "NeisApi",
    "ProjectApi",
    "ProjectRequest",
    "ScheduleRequest",
    "StudentApi",
    "StudentRequest",
    "TimetableRequest",
]
