## DataGSM OpenAPI SDK for Python
[![PyPI](https://img.shields.io/pypi/v/datagsm-openapi-sdk)](https://pypi.org/project/datagsm-openapi-sdk/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

DataGSM의 OpenAPI를 추상화된 환경에서 제공합니다.

### 설치 - pip

```bash
pip install datagsm-openapi-sdk
```

### 설치 - uv
```bash
uv pip install datagsm-openapi-sdk
```

### 빠른 시작

```python
from datetime import date

from datagsm_openapi import DataGsmClient, ProjectRequest, TimetableRequest

with DataGsmClient(api_key="your-api-key") as client:
    students = client.students.get_students()
    projects = client.projects.get_projects(ProjectRequest(club_id=1))
    timetables = client.neis.get_timetables(
        TimetableRequest(grade=1, class_num=1, from_date=date(2026, 4, 6), to_date=date(2026, 4, 10))
    )
```

학생·동아리·프로젝트의 생성·수정·삭제 메서드는 해당 `*_WRITE` 스코프가 있는 API 키에서만 동작합니다.

### 사용법
자세한 사용법은 [기술 문서](https://docs.datagsm.kr/api/sdk/python)를 참고하십시오.
