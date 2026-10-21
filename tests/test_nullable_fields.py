"""Nullable response fields must match datagsm-server DTO nullability."""

import pytest
from pydantic import ValidationError

from datagsm_openapi import DataGsmClient
from datagsm_openapi.models import ClubDetail, Meal, ParticipantInfo, Student

from . import payloads
from .conftest import RecordingTransport


def test_student_accepts_null_student_number_fields() -> None:
    student = Student.model_validate(
        payloads.student(
            grade=None,
            classNum=None,
            number=None,
            studentNumber=None,
            major=None,
            role="GRADUATE",
            dormitoryFloor=None,
            dormitoryRoom=None,
            majorClub=None,
            githubId=None,
            githubUrl=None,
            specialty=None,
        )
    )

    assert student.grade is None
    assert student.class_num is None
    assert student.number is None
    assert student.student_number is None
    assert student.major is None


def test_student_grade_still_validates_range() -> None:
    with pytest.raises(ValidationError):
        Student.model_validate(payloads.student(grade=4))


def test_participant_accepts_null_student_number_and_major() -> None:
    participant = ParticipantInfo.model_validate(
        payloads.participant(studentNumber=None, major=None)
    )

    assert participant.student_number is None
    assert participant.major is None


def test_club_detail_accepts_null_leader() -> None:
    club = ClubDetail.model_validate(
        payloads.club(leader=None, participants=[], status="ABOLISHED", abolishedYear=2024)
    )

    assert club.leader is None


def test_meal_accepts_null_allergy_info() -> None:
    meal = Meal.model_validate(payloads.meal(mealAllergyInfo=None))

    assert meal.meal_allergy_info is None


def test_student_list_with_graduate_parses(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    graduate = payloads.student(
        id=2, grade=None, classNum=None, number=None, studentNumber=None, role="GRADUATE"
    )
    transport.queue_data(payloads.page("students", [payloads.student(), graduate]))

    response = client.students.get_students()

    assert [s.grade for s in response.students] == [1, None]
