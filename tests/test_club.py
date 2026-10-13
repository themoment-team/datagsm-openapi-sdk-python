"""Club API tests."""

from datagsm_openapi import ClubRequest, DataGsmClient
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


def test_get_club_returns_first_match(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("clubs", [payloads.club(id=7)]))

    club = client.clubs.get_club(7)

    assert club is not None
    assert club.id == 7
    assert transport.last.url.params["clubId"] == "7"
