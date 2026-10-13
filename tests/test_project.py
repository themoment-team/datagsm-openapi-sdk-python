"""Project API query and response tests."""

import json
from typing import Any

import pytest

from datagsm_openapi import (
    BadRequestException,
    ConflictException,
    DataGsmClient,
    EndProjectRequest,
    NotFoundException,
    ProjectRequest,
    ProjectWriteRequest,
)
from datagsm_openapi.models import Project, ProjectCategory, ProjectStatus

from . import payloads
from .conftest import RecordingTransport


def test_project_parses_categories_and_new_fields() -> None:
    project = Project.model_validate(payloads.project())

    assert project.categories == [ProjectCategory.TEAM, ProjectCategory.CLUB]
    assert all(isinstance(c, ProjectCategory) for c in project.categories)
    assert project.icon_url == "https://cdn.datagsm.kr/project-icons/uuid.png"
    assert project.icon_key == "project-icons/uuid.png"
    assert project.deployment_url == "https://datagsm.kr"


def test_project_categories_default_to_empty_list() -> None:
    data = payloads.project()
    for key in ("categories", "iconUrl", "iconKey", "deploymentUrl"):
        data.pop(key)

    project = Project.model_validate(data)

    assert project.categories == []
    assert project.icon_url is None
    assert project.deployment_url is None


def test_unknown_category_is_kept_as_string(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(
        payloads.page("projects", [payloads.project(categories=["TEAM", "HACKATHON"])])
    )

    response = client.projects.get_projects()

    categories = response.projects[0].categories
    assert categories == [ProjectCategory.TEAM, "HACKATHON"]
    assert isinstance(categories[0], ProjectCategory)
    assert not isinstance(categories[1], ProjectCategory)


def test_category_filter_is_serialized(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("projects", []))

    client.projects.get_projects(ProjectRequest(category=ProjectCategory.IDEA_FESTIVAL))

    params = transport.last.url.params
    assert transport.last.url.path == "/v1/projects"
    assert params["category"] == "IDEA_FESTIVAL"
    assert params["status"] == "ACTIVE"


def test_category_filter_accepts_raw_string(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("projects", []))

    client.projects.get_projects(ProjectRequest(category="NEW_CATEGORY", status=None))

    params = transport.last.url.params
    assert params["category"] == "NEW_CATEGORY"
    assert "status" not in params


def test_category_filter_omitted_by_default(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("projects", []))

    client.projects.get_projects()

    assert "category" not in transport.last.url.params


def test_get_project_falls_back_to_ended(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("projects", []))
    transport.queue_data(
        payloads.page("projects", [payloads.project(id=3, status="ENDED", endYear=2025)])
    )

    project = client.projects.get_project(3)

    assert project is not None
    assert project.status == ProjectStatus.ENDED
    statuses = [r.url.params["status"] for r in transport.requests]
    assert statuses == ["ACTIVE", "ENDED"]


def test_get_project_returns_active_without_second_request(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("projects", [payloads.project(id=3)]))

    project = client.projects.get_project(3)

    assert project is not None
    assert len(transport.requests) == 1


def test_get_project_returns_none_when_missing(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.page("projects", []))
    transport.queue_data(payloads.page("projects", []))

    assert client.projects.get_project(404) is None


def _project_request(**overrides: Any) -> ProjectWriteRequest:
    fields: dict[str, Any] = {
        "name": "DataGSM",
        "description": "학교 데이터를 제공하는 API 서비스",
        "start_year": 2024,
        "club_id": 1,
        "participant_ids": [1, 2],
    }
    fields.update(overrides)
    return ProjectWriteRequest(**fields)


def test_create_project_body_omits_unset_optional_fields(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.project(id=21, categories=[]))

    project = client.projects.create_project(_project_request())

    assert transport.last.method == "POST"
    assert transport.last.url.path == "/v1/projects"
    assert transport.last_json() == {
        "name": "DataGSM",
        "description": "학교 데이터를 제공하는 API 서비스",
        "startYear": 2024,
        "clubId": 1,
        "participantIds": [1, 2],
        "status": "ACTIVE",
        "endYear": None,
        "repositories": [],
        "techStacks": [],
    }
    assert project.id == 21
    assert project.categories == []


def test_project_body_sends_categories_and_icon_fields(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.project())

    client.projects.create_project(
        _project_request(
            categories=[ProjectCategory.TEAM, "CLUB"],
            icon_key="project-icons/uuid.png",
            deployment_url="https://datagsm.kr",
            repositories=["https://github.com/team/repo"],
            tech_stacks=["Kotlin"],
        )
    )

    body = transport.last_json()
    assert body["categories"] == ["TEAM", "CLUB"]
    assert body["iconKey"] == "project-icons/uuid.png"
    assert body["deploymentUrl"] == "https://datagsm.kr"
    assert body["repositories"] == ["https://github.com/team/repo"]
    assert body["techStacks"] == ["Kotlin"]


def test_update_project_distinguishes_none_and_empty(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.project(categories=[]))
    transport.queue_data(payloads.project())

    client.projects.update_project(
        5, _project_request(categories=[], icon_key="", deployment_url="")
    )
    cleared = transport.last_json()
    client.projects.update_project(5, _project_request(categories=None))
    kept = transport.last_json()

    assert transport.last.method == "PUT"
    assert transport.last.url.path == "/v1/projects/5"
    assert cleared["categories"] == []
    assert cleared["iconKey"] == ""
    assert cleared["deploymentUrl"] == ""
    assert "categories" not in kept
    assert "iconKey" not in kept
    assert "deploymentUrl" not in kept


def test_project_categories_rejects_single_string() -> None:
    with pytest.raises(TypeError):
        _project_request(categories="TEAM").to_body()


def test_create_ended_project_sends_end_year(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue_data(payloads.project(status="ENDED", endYear=2025))

    client.projects.create_project(
        _project_request(status=ProjectStatus.ENDED, end_year=2025, club_id=None)
    )

    body = transport.last_json()
    assert body["status"] == "ENDED"
    assert body["endYear"] == 2025
    assert body["clubId"] is None


@pytest.mark.parametrize(
    ("status_code", "content"),
    [(204, b""), (200, b""), (200, b'{"status":"OK","code":200,"message":"OK"}')],
)
def test_project_no_content_endpoints(
    client: DataGsmClient, transport: RecordingTransport, status_code: int, content: bytes
) -> None:
    for _ in range(3):
        transport.queue(status_code, content=content)

    client.projects.end_project(7, EndProjectRequest(end_year=2025))
    end_request = transport.last
    client.projects.reactivate_project(7)
    reactivate_request = transport.last
    client.projects.delete_project(7)
    delete_request = transport.last

    assert (end_request.method, end_request.url.path) == ("POST", "/v1/projects/7/end")
    assert json.loads(end_request.content) == {"endYear": 2025}
    assert (reactivate_request.method, reactivate_request.url.path) == (
        "POST",
        "/v1/projects/7/reactivate",
    )
    assert (delete_request.method, delete_request.url.path) == ("DELETE", "/v1/projects/7")


def test_end_project_bad_request(client: DataGsmClient, transport: RecordingTransport) -> None:
    message = "종료 연도는 시작 연도보다 크거나 같아야 합니다."
    transport.queue(400, {"status": "BAD_REQUEST", "code": 400, "message": message})

    with pytest.raises(BadRequestException) as exc_info:
        client.projects.end_project(7, EndProjectRequest(end_year=2000))

    assert exc_info.value.message == message


def test_update_project_conflict(client: DataGsmClient, transport: RecordingTransport) -> None:
    message = "이미 존재하는 프로젝트 이름입니다."
    transport.queue(409, {"status": "CONFLICT", "code": 409, "message": message})

    with pytest.raises(ConflictException):
        client.projects.update_project(5, _project_request())


def test_reactivate_project_not_found(client: DataGsmClient, transport: RecordingTransport) -> None:
    message = "프로젝트를 찾을 수 없습니다."
    transport.queue(404, {"status": "NOT_FOUND", "code": 404, "message": message})

    with pytest.raises(NotFoundException):
        client.projects.reactivate_project(999)
