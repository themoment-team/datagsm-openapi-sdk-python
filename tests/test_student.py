"""Student API tests."""

from datagsm_openapi import DataGsmClient, StudentRequest
from datagsm_openapi.models import Major, StudentRole

from . import payloads
from .conftest import RecordingTransport


def test_student_filters_are_serialized(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("students", [payloads.student()]))

    client.students.get_students(
        StudentRequest(
            grade=1,
            major=Major.AI,
            role=StudentRole.GENERAL_STUDENT,
            include_graduates=True,
            include_withdrawn=False,
            only_enrolled=False,
        )
    )

    params = transport.last.url.params
    assert transport.last.url.path == "/v1/students"
    assert params["includeGraduates"] == "true"
    assert params["includeWithdrawn"] == "false"
    assert params["onlyEnrolled"] == "false"
    assert params["major"] == "AI"
    assert params["size"] == "300"


def test_student_default_omits_include_flags(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("students", []))

    client.students.get_students()

    params = transport.last.url.params
    assert "includeGraduates" not in params
    assert "includeWithdrawn" not in params


def test_get_student_includes_graduates_and_withdrawn(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    graduate = payloads.student(
        id=5, grade=None, classNum=None, number=None, studentNumber=None, role="GRADUATE"
    )
    transport.queue_data(payloads.page("students", [graduate]))

    student = client.students.get_student(5)

    params = transport.last.url.params
    assert params["studentId"] == "5"
    assert params["includeGraduates"] == "true"
    assert params["includeWithdrawn"] == "true"
    assert student is not None
    assert student.role == StudentRole.GRADUATE


def test_get_student_returns_none_when_missing(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("students", []))

    assert client.students.get_student(999) is None
