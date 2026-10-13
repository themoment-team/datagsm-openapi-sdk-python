"""Shared test fixtures for DataGSM OpenAPI SDK."""

import json
from collections.abc import Iterator
from typing import Any, Optional

import httpx
import pytest

from datagsm_openapi import DataGsmClient

BASE_URL = "https://openapi.test"


class RecordingTransport:
    """httpx.MockTransport wrapper that records requests and replays canned responses."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self._responses: list[httpx.Response] = []

    def queue(
        self,
        status_code: int = 200,
        json_body: Optional[Any] = None,
        content: Optional[bytes] = None,
    ) -> None:
        if json_body is not None:
            self._responses.append(httpx.Response(status_code, json=json_body))
        else:
            self._responses.append(httpx.Response(status_code, content=content or b""))

    def queue_data(self, data: Any) -> None:
        self.queue(200, {"status": "OK", "code": 200, "message": "OK", "data": data})

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if not self._responses:
            raise AssertionError(f"Unexpected request: {request.method} {request.url}")
        return self._responses.pop(0)

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]

    def last_json(self) -> Any:
        return json.loads(self.last.content)


@pytest.fixture
def transport() -> RecordingTransport:
    return RecordingTransport()


@pytest.fixture
def client(transport: RecordingTransport) -> Iterator[DataGsmClient]:
    sdk_client = DataGsmClient(api_key="test-key", base_url=BASE_URL)
    http = sdk_client._http_client
    http._client = httpx.Client(
        base_url=http.base_url,
        headers=http._get_headers(),
        transport=httpx.MockTransport(transport.handler),
    )
    yield sdk_client
    sdk_client.close()
