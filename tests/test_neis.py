"""NEIS API request/response tests."""

from datetime import date

import pytest

from datagsm_openapi import DataGsmClient, MealRequest, ScheduleRequest, TimetableRequest

from . import payloads
from .conftest import RecordingTransport


def test_timetable_range_uses_from_and_to_date(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data({"timetables": [payloads.timetable()]})

    timetables = client.neis.get_timetables(
        TimetableRequest(
            grade=2, class_num=3, from_date=date(2026, 4, 7), to_date=date(2026, 4, 11)
        )
    )

    params = transport.last.url.params
    assert transport.last.url.path == "/v1/neis/timetables"
    assert params["grade"] == "2"
    assert params["classNum"] == "3"
    assert params["fromDate"] == "2026-04-07"
    assert params["toDate"] == "2026-04-11"
    assert "startDate" not in params
    assert "endDate" not in params
    assert "date" not in params
    assert len(timetables) == 1


def test_timetable_requires_grade_and_class_num() -> None:
    with pytest.raises(TypeError):
        TimetableRequest(date=date(2026, 4, 7))  # type: ignore[call-arg]


def test_timetable_single_date(client: DataGsmClient, transport: RecordingTransport) -> None:
    transport.queue_data({"timetables": []})

    client.neis.get_timetables(TimetableRequest(grade=1, class_num=1, date=date(2026, 4, 7)))

    params = transport.last.url.params
    assert params["date"] == "2026-04-07"
    assert "fromDate" not in params


def test_meal_range_params(client: DataGsmClient, transport: RecordingTransport) -> None:
    transport.queue_data({"meals": [payloads.meal()]})

    meals = client.neis.get_meals(
        MealRequest(from_date=date(2026, 2, 1), to_date=date(2026, 2, 7))
    )

    params = transport.last.url.params
    assert params["fromDate"] == "2026-02-01"
    assert params["toDate"] == "2026-02-07"
    assert meals[0].meal_allergy_info == ["1", "2"]


def test_schedule_single_date(client: DataGsmClient, transport: RecordingTransport) -> None:
    transport.queue_data({"schedules": []})

    schedules = client.neis.get_schedules(ScheduleRequest(date=date(2026, 3, 1)))

    assert transport.last.url.params["date"] == "2026-03-01"
    assert schedules == []
