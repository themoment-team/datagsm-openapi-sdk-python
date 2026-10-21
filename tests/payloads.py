"""Sample server payloads mirroring datagsm-server response DTOs."""

from typing import Any


def participant(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": 1,
        "name": "홍길동",
        "email": "s24001@gsm.hs.kr",
        "studentNumber": 1101,
        "major": "SW_DEVELOPMENT",
        "sex": "MAN",
    }
    data.update(overrides)
    return data


def student(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": 1,
        "name": "홍길동",
        "sex": "MAN",
        "email": "s24001@gsm.hs.kr",
        "grade": 1,
        "classNum": 1,
        "number": 1,
        "studentNumber": 1101,
        "major": "SW_DEVELOPMENT",
        "specialty": "백엔드",
        "role": "GENERAL_STUDENT",
        "dormitoryFloor": 3,
        "dormitoryRoom": 301,
        "majorClub": {"id": 1, "name": "SW개발동아리", "type": "MAJOR_CLUB"},
        "autonomousClub": None,
        "githubId": "torvalds",
        "githubUrl": "https://github.com/torvalds",
    }
    data.update(overrides)
    return data


def club(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": 1,
        "name": "SW개발동아리",
        "type": "MAJOR_CLUB",
        "leader": participant(),
        "participants": [participant(id=2, studentNumber=1102)],
        "foundedYear": 2022,
        "status": "ACTIVE",
        "abolishedYear": None,
    }
    data.update(overrides)
    return data


def project(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": 1,
        "name": "DataGSM",
        "description": "학교 데이터를 제공하는 API 서비스",
        "startYear": 2024,
        "endYear": None,
        "status": "ACTIVE",
        "categories": ["TEAM", "CLUB"],
        "iconUrl": "https://cdn.datagsm.kr/project-icons/uuid.png",
        "iconKey": "project-icons/uuid.png",
        "deploymentUrl": "https://datagsm.kr",
        "club": {"id": 1, "name": "SW개발동아리", "type": "MAJOR_CLUB"},
        "participants": [participant()],
        "repositories": ["https://github.com/themoment-team/datagsm-server"],
        "techStacks": ["Kotlin", "Spring Boot"],
    }
    data.update(overrides)
    return data


def meal(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "mealId": "7430310_20251215_2",
        "schoolCode": "7430310",
        "schoolName": "광주소프트웨어마이스터고등학교",
        "officeCode": "G10",
        "officeName": "광주광역시교육청",
        "mealDate": "2025-12-15",
        "mealType": "LUNCH",
        "mealMenu": ["쌀밥", "김치찌개"],
        "mealAllergyInfo": ["1", "2"],
        "mealCalories": "650.8 Kcal",
        "originInfo": None,
        "nutritionInfo": None,
        "mealServeCount": None,
    }
    data.update(overrides)
    return data


def timetable(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "timetableId": "7380292_20250303_1_1_1",
        "schoolCode": "7380292",
        "schoolName": "광주소프트웨어마이스터고등학교",
        "officeCode": "F10",
        "officeName": "광주광역시교육청",
        "timetableDate": "2025-03-03",
        "academicYear": "2025",
        "semester": None,
        "grade": 1,
        "classNum": 1,
        "period": 1,
        "subject": None,
    }
    data.update(overrides)
    return data


def page(key: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    return {"totalPages": 1, "totalElements": len(items), key: items}
