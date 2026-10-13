"""Club API tests."""

import pytest

from datagsm_openapi import (
    ClubRequest,
    ClubWriteRequest,
    ConflictException,
    DataGsmClient,
    NotFoundException,
)
from datagsm_openapi.models import ClubSortBy, ClubStatus, ClubType

from . import payloads
from .conftest import RecordingTransport


def test_club_status_filter_uses_club_status_key(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("clubs", [payloads.club()]))

    client.clubs.get_clubs(
        ClubRequest(
            club_type=ClubType.MAJOR_CLUB,
            status=ClubStatus.ABOLISHED,
            founded_year=2022,
            sort_by=ClubSortBy.FOUNDED_YEAR,
        )
    )

    params = transport.last.url.params
    assert transport.last.url.path == "/v1/clubs"
    assert params["clubStatus"] == "ABOLISHED"
    assert "status" not in params
    assert params["foundedYear"] == "2022"
    assert params["clubType"] == "MAJOR_CLUB"
    assert params["sortBy"] == "FOUNDED_YEAR"


def test_club_default_params_omit_optional_filters(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("clubs", []))

    client.clubs.get_clubs()

    params = transport.last.url.params
    assert "clubStatus" not in params
    assert "foundedYear" not in params
    assert params["page"] == "0"
    assert params["size"] == "100"


def test_club_sort_by_matches_server_enum() -> None:
    assert {member.value for member in ClubSortBy} == {
        "ID",
        "NAME",
        "TYPE",
        "FOUNDED_YEAR",
        "STATUS",
    }


def test_get_club_returns_first_match(client: DataGsmClient, transport: RecordingTransport) -> None:
    transport.queue_data(payloads.page("clubs", [payloads.club(id=7)]))

    club = client.clubs.get_club(7)

    assert club is not None
    assert club.id == 7
    assert transport.last.url.params["clubId"] == "7"


def _active_club_request() -> ClubWriteRequest:
    return ClubWriteRequest(
        name="SW개발동아리",
        type=ClubType.MAJOR_CLUB,
        founded_year=2022,
        status=ClubStatus.ACTIVE,
        leader_id=1,
        participant_ids=[2, 3],
    )


def test_create_club_sends_body(client: DataGsmClient, transport: RecordingTransport) -> None:
    transport.queue_data(payloads.club(id=11))

    club = client.clubs.create_club(_active_club_request())

    assert transport.last.method == "POST"
    assert transport.last.url.path == "/v1/clubs"
    assert transport.last_json() == {
        "name": "SW개발동아리",
        "type": "MAJOR_CLUB",
        "leaderId": 1,
        "participantIds": [2, 3],
        "foundedYear": 2022,
        "status": "ACTIVE",
        "abolishedYear": None,
    }
    assert club.id == 11


def test_update_abolished_club_sends_null_leader(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(
        payloads.club(leader=None, participants=[], status="ABOLISHED", abolishedYear=2024)
    )

    club = client.clubs.update_club(
        4,
        ClubWriteRequest(
            name="폐지동아리",
            type=ClubType.AUTONOMOUS_CLUB,
            founded_year=2020,
            status=ClubStatus.ABOLISHED,
            abolished_year=2024,
        ),
    )

    body = transport.last_json()
    assert transport.last.method == "PUT"
    assert transport.last.url.path == "/v1/clubs/4"
    assert body["leaderId"] is None
    assert body["participantIds"] == []
    assert body["abolishedYear"] == 2024
    assert club.leader is None


@pytest.mark.parametrize(
    ("status_code", "content"),
    [(204, b""), (200, b""), (200, b'{"status":"OK","code":200,"message":"OK"}')],
)
def test_delete_club_accepts_empty_or_envelope_body(
    client: DataGsmClient, transport: RecordingTransport, status_code: int, content: bytes
) -> None:
    transport.queue(status_code, content=content)

    client.clubs.delete_club(4)
    assert transport.last.method == "DELETE"
    assert transport.last.url.path == "/v1/clubs/4"


def test_delete_club_not_found(client: DataGsmClient, transport: RecordingTransport) -> None:
    transport.queue(
        404, {"status": "NOT_FOUND", "code": 404, "message": "동아리를 찾을 수 없습니다."}
    )

    with pytest.raises(NotFoundException):
        client.clubs.delete_club(999)


def test_create_club_conflict(client: DataGsmClient, transport: RecordingTransport) -> None:
    transport.queue(
        409, {"status": "CONFLICT", "code": 409, "message": "이미 존재하는 동아리 이름입니다."}
    )

    with pytest.raises(ConflictException) as exc_info:
        client.clubs.create_club(_active_club_request())

    assert exc_info.value.message == "이미 존재하는 동아리 이름입니다."
