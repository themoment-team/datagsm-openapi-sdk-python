"""HTTP layer tests: error mapping and empty response bodies."""

from typing import Any

import httpx
import pytest

from datagsm_openapi import (
    BadRequestException,
    ConflictException,
    DataGsmClient,
    DataGsmException,
    ForbiddenException,
    NetworkException,
    NotFoundException,
    RateLimitException,
    ServerErrorException,
    UnauthorizedException,
    ValidationException,
)
from datagsm_openapi.api._base import BaseApi
from datagsm_openapi.models import Student

from . import payloads
from .conftest import RecordingTransport


def _error_body(code: int, message: str) -> dict[str, Any]:
    return {"status": "ERROR", "code": code, "message": message}


@pytest.mark.parametrize(
    ("status_code", "exception_type"),
    [
        (400, BadRequestException),
        (401, UnauthorizedException),
        (403, ForbiddenException),
        (404, NotFoundException),
        (409, ConflictException),
        (429, RateLimitException),
        (500, ServerErrorException),
        (503, ServerErrorException),
        (418, DataGsmException),
    ],
)
def test_error_status_maps_to_exception(
    client: DataGsmClient,
    transport: RecordingTransport,
    status_code: int,
    exception_type: type[DataGsmException],
) -> None:
    transport.queue(status_code, _error_body(status_code, "이미 존재하는 이메일입니다."))

    with pytest.raises(exception_type) as exc_info:
        client.students.get_students()

    assert exc_info.value.status_code == status_code
    assert exc_info.value.message == "이미 존재하는 이메일입니다."
    assert exc_info.value.response_body is not None


def test_error_without_json_body_uses_text(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue(502, content=b"Bad Gateway")

    with pytest.raises(ServerErrorException) as exc_info:
        client.students.get_students()

    assert exc_info.value.message == "Bad Gateway"
    assert exc_info.value.response_body is None


def test_error_with_non_object_json_body(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue(400, ["unexpected"])

    with pytest.raises(BadRequestException) as exc_info:
        client.students.get_students()

    assert exc_info.value.response_body is None


def test_conflict_exception_is_exported_and_subclasses_base() -> None:
    error = ConflictException()

    assert isinstance(error, DataGsmException)
    assert error.status_code == 409


@pytest.mark.parametrize(
    ("status_code", "content"),
    [(204, b""), (200, b""), (200, b"  \n")],
)
def test_empty_body_returns_none(
    client: DataGsmClient, transport: RecordingTransport, status_code: int, content: bytes
) -> None:
    transport.queue(status_code, content=content)

    assert client._http_client.request("DELETE", "/v1/clubs/1") is None


def test_no_content_helper_accepts_envelope_without_data(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue(200, {"status": "OK", "code": 200, "message": "OK"})

    BaseApi(client._http_client)._send_no_content("POST", "/v1/projects/1/reactivate")

    assert transport.last.method == "POST"


def test_data_endpoint_with_empty_body_raises_validation(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue(204)

    with pytest.raises(ValidationException):
        BaseApi(client._http_client)._send("POST", "/v1/students", Student, body={})


def test_invalid_json_success_body_raises_validation(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue(200, content=b"<html>oops</html>")

    with pytest.raises(ValidationException):
        client.students.get_students()


def test_envelope_without_data_raises_validation(
    client: DataGsmClient, transport: RecordingTransport
) -> None:
    transport.queue(200, {"status": "OK", "code": 200, "message": "OK"})

    with pytest.raises(ValidationException):
        client.students.get_students()


def test_network_error_is_wrapped(client: DataGsmClient) -> None:
    def fail(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    http = client._http_client
    http._client = httpx.Client(base_url=http.base_url, transport=httpx.MockTransport(fail))

    with pytest.raises(NetworkException):
        client.students.get_students()


def test_api_key_header_is_sent(client: DataGsmClient, transport: RecordingTransport) -> None:
    transport.queue_data(payloads.page("students", []))

    client.students.get_students()

    assert transport.last.headers["X-API-KEY"] == "test-key"
