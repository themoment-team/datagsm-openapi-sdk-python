"""Project API query and response tests."""

from datagsm_openapi import DataGsmClient, ProjectRequest
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
