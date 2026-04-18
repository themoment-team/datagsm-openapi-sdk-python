"""NEIS API module for DataGSM OpenAPI SDK."""

from dataclasses import dataclass
from datetime import date as Date
from typing import Optional

from ..models import Meal, MealResponse, Schedule, ScheduleResponse, Timetable, TimetableResponse
from ._base import BaseApi


@dataclass
class MealRequest:
    """급식 조회 요청 파라미터 (Meal Query Parameters).

    Use either 'date' for a single day or 'from_date' and 'to_date' for a date range.

    Attributes:
        date: Single date to query
        from_date: Start date for range query
        to_date: End date for range query
    """

    date: Optional[Date] = None
    from_date: Optional[Date] = None
    to_date: Optional[Date] = None

    def to_params(self) -> dict[str, Optional[object]]:
        """Convert to query parameters dictionary.

        Returns:
            Dictionary of query parameters
        """
        params: dict[str, Optional[object]] = {
            "date": self.date,
            "fromDate": self.from_date,
            "toDate": self.to_date,
        }
        return params


@dataclass
class ScheduleRequest:
    """학사일정 조회 요청 파라미터 (Schedule Query Parameters).

    Use either 'date' for a single day or 'from_date' and 'to_date' for a date range.

    Attributes:
        date: Single date to query
        from_date: Start date for range query
        to_date: End date for range query
    """

    date: Optional[Date] = None
    from_date: Optional[Date] = None
    to_date: Optional[Date] = None

    def to_params(self) -> dict[str, Optional[object]]:
        """Convert to query parameters dictionary.

        Returns:
            Dictionary of query parameters
        """
        params: dict[str, Optional[object]] = {
            "date": self.date,
            "fromDate": self.from_date,
            "toDate": self.to_date,
        }
        return params


@dataclass
class TimetableRequest:
    """시간표 조회 요청 파라미터 (Timetable Query Parameters).

    Use either 'date' for a single day or 'start_date' and 'end_date' for a date range.
    Either 'date' or both 'start_date' and 'end_date' must be provided.

    Attributes:
        grade: Grade to query (1-3)
        class_num: Class number to query (1-4)
        date: Single date to query
        start_date: Start date for range query
        end_date: End date for range query
    """

    grade: int = 0
    class_num: int = 0
    date: Optional[Date] = None
    start_date: Optional[Date] = None
    end_date: Optional[Date] = None

    def to_params(self) -> dict[str, Optional[object]]:
        """Convert to query parameters dictionary.

        Returns:
            Dictionary of query parameters
        """
        params: dict[str, Optional[object]] = {
            "grade": self.grade,
            "classNum": self.class_num,
            "date": self.date,
            "startDate": self.start_date,
            "endDate": self.end_date,
        }
        return params


class NeisApi(BaseApi):
    """NEIS 데이터 API (NEIS Data API).

    Provides methods for querying school meal, schedule, and timetable information from NEIS.
    """

    def get_meals(self, request: Optional[MealRequest] = None) -> list[Meal]:
        """급식 정보 조회 (Get Meal Information).

        Query school meal information for a specific date or date range.

        Args:
            request: Query parameters (optional, defaults to today)

        Returns:
            List of meals

        Example:
            >>> from datetime import date
            >>> api = NeisApi(http_client)
            >>>
            >>> # Get today's meals
            >>> today_meals = api.get_meals()
            >>>
            >>> # Get meals for a specific date
            >>> request = MealRequest(date=date(2026, 2, 3))
            >>> meals = api.get_meals(request)
            >>>
            >>> # Get meals for a date range
            >>> request = MealRequest(
            ...     from_date=date(2026, 2, 1),
            ...     to_date=date(2026, 2, 7)
            ... )
            >>> week_meals = api.get_meals(request)
        """
        req = request or MealRequest(date=Date.today())
        response = self._get(
            "/v1/neis/meals", params=req.to_params(), response_type=MealResponse
        )
        return response.meals

    def get_schedules(self, request: Optional[ScheduleRequest] = None) -> list[Schedule]:
        """학사일정 정보 조회 (Get Schedule Information).

        Query school schedule/event information for a specific date or date range.

        Args:
            request: Query parameters (optional, defaults to today)

        Returns:
            List of schedules

        Example:
            >>> from datetime import date
            >>> api = NeisApi(http_client)
            >>>
            >>> # Get today's schedules
            >>> today_events = api.get_schedules()
            >>>
            >>> # Get schedules for a specific date
            >>> request = ScheduleRequest(date=date(2026, 3, 1))
            >>> schedules = api.get_schedules(request)
            >>>
            >>> # Get schedules for a date range
            >>> request = ScheduleRequest(
            ...     from_date=date(2026, 3, 1),
            ...     to_date=date(2026, 3, 31)
            ... )
            >>> month_schedules = api.get_schedules(request)
        """
        req = request or ScheduleRequest(date=Date.today())
        response = self._get(
            "/v1/neis/schedules", params=req.to_params(), response_type=ScheduleResponse
        )
        return response.schedules

    def get_timetables(self, request: TimetableRequest) -> list[Timetable]:
        """시간표 정보 조회 (Get Timetable Information).

        Query school timetable information for a specific grade, class, and date or date range.
        Either 'date' or both 'start_date' and 'end_date' must be provided in the request.

        Args:
            request: Query parameters (grade, class_num, and date/date range are required)

        Returns:
            List of timetables

        Example:
            >>> from datetime import date
            >>> api = NeisApi(http_client)
            >>>
            >>> # Get timetable for a specific date
            >>> request = TimetableRequest(grade=1, class_num=1, date=date(2026, 4, 7))
            >>> timetables = api.get_timetables(request)
            >>>
            >>> # Get timetables for a date range
            >>> request = TimetableRequest(
            ...     grade=2,
            ...     class_num=3,
            ...     start_date=date(2026, 4, 7),
            ...     end_date=date(2026, 4, 11)
            ... )
            >>> week_timetables = api.get_timetables(request)
        """
        response = self._get(
            "/v1/neis/timetables", params=request.to_params(), response_type=TimetableResponse
        )
        return response.timetables
