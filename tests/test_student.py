"""Student API tests."""

import pytest

from datagsm_openapi import (
    ConflictException,
    CreateStudentRequest,
    DataGsmClient,
    NotFoundException,
    StudentRequest,
    UpdateStudentRequest,
)
from datagsm_openapi.models import Major, Sex, StudentRole

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


def test_create_student_sends_body_and_parses_response(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.student(id=10))

    student = client.students.create_student(
        CreateStudentRequest(
            name="홍길동",
            sex=Sex.MAN,
            email="s24001@gsm.hs.kr",
            grade=1,
            class_num=1,
            number=1,
            dormitory_room_number=301,
            major_club_id=1,
        )
    )

    assert transport.last.method == "POST"
    assert transport.last.url.path == "/v1/students"
    assert transport.last_json() == {
        "name": "홍길동",
        "sex": "MAN",
        "email": "s24001@gsm.hs.kr",
        "grade": 1,
        "classNum": 1,
        "number": 1,
        "role": "GENERAL_STUDENT",
        "dormitoryRoomNumber": 301,
        "majorClubId": 1,
        "autonomousClubId": None,
        "specialty": None,
    }
    assert student.id == 10


def test_create_graduate_without_student_number(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(
        payloads.student(grade=None, classNum=None, number=None, studentNumber=None)
    )

    client.students.create_student(
        CreateStudentRequest(
            name="졸업생", sex=Sex.WOMAN, email="g@gsm.hs.kr", role=StudentRole.GRADUATE
        )
    )

    body = transport.last_json()
    assert body["role"] == "GRADUATE"
    assert body["grade"] is None


def test_update_student_sends_put(client: DataGsmClient, transport: RecordingTransport) -> None:
    transport.queue_data(payloads.student(id=3, githubId="octocat"))

    student = client.students.update_student(
        3,
        UpdateStudentRequest(
            name="홍길동",
            sex=Sex.MAN,
            email="s24001@gsm.hs.kr",
            grade=2,
            class_num=4,
            number=18,
            role=StudentRole.STUDENT_COUNCIL,
            github_id="octocat",
        ),
    )

    body = transport.last_json()
    assert transport.last.method == "PUT"
    assert transport.last.url.path == "/v1/students/3"
    assert body["classNum"] == 4
    assert body["role"] == "STUDENT_COUNCIL"
    assert body["githubId"] == "octocat"
    assert body["dormitoryRoomNumber"] is None
    assert student.github_id == "octocat"


def test_create_student_conflict(client: DataGsmClient, transport: RecordingTransport) -> None:
    transport.queue(
        409, {"status": "CONFLICT", "code": 409, "message": "이미 존재하는 이메일입니다."}
    )

    with pytest.raises(ConflictException):
        client.students.create_student(
            CreateStudentRequest(
                name="a", sex=Sex.MAN, email="a@gsm.hs.kr", grade=1, class_num=1, number=1
            )
        )


def test_update_student_not_found(client: DataGsmClient, transport: RecordingTransport) -> None:
    transport.queue(
        404, {"status": "NOT_FOUND", "code": 404, "message": "학생을 찾을 수 없습니다."}
    )

    with pytest.raises(NotFoundException):
        client.students.update_student(
            999,
            UpdateStudentRequest(
                name="a",
                sex=Sex.MAN,
                email="a@gsm.hs.kr",
                grade=1,
                class_num=1,
                number=1,
                role=StudentRole.GENERAL_STUDENT,
            ),
        )
