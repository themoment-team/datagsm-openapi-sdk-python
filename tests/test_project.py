"""Project API query and response tests."""

from datagsm_openapi import DataGsmClient, ProjectRequest
from datagsm_openapi.models import Project, ProjectCategory

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
