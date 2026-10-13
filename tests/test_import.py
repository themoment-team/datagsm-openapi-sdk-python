"""Package import smoke tests."""

import importlib
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_package_imports_in_fresh_interpreter() -> None:
    result = subprocess.run(
        [sys.executable, "-I", "-c", "import datagsm_openapi; print(datagsm_openapi.__version__)"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip()


def test_submodules_import_first_in_fresh_interpreter() -> None:
    for module in ("datagsm_openapi._http", "datagsm_openapi.client", "datagsm_openapi.api"):
        result = subprocess.run(
            [sys.executable, "-I", "-c", f"import {module}"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"{module}: {result.stderr}"


def test_version_matches_pyproject() -> None:
    package = importlib.import_module("datagsm_openapi")
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.MULTILINE)

    assert match is not None
    assert package.__version__ == match.group(1)


def test_user_agent_contains_version() -> None:
    from datagsm_openapi._http import HttpClient
    from datagsm_openapi._version import __version__

    headers = HttpClient(base_url="https://example.test", api_key="k")._get_headers()

    assert headers["User-Agent"] == f"datagsm-openapi-sdk-python/{__version__}"
