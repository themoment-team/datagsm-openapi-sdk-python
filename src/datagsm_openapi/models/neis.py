"""NEIS-related models (급식, 학사일정, 시간표) for DataGSM OpenAPI SDK."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .enums import MealType


class Meal(BaseModel):
    """급식 정보 (Meal Information).

    Information about school meals from NEIS.

    Attributes:
        meal_id: Meal ID
        school_code: School code
        school_name: School name
        office_code: Education office code
        office_name: Education office name
        meal_date: Meal date
        meal_type: Meal type (BREAKFAST, LUNCH, DINNER)
        meal_menu: List of menu items
        meal_allergy_info: List of allergy information
        meal_calories: Calorie information
        origin_info: Origin information of ingredients
        nutrition_info: Nutrition information
        meal_serve_count: Number of servings
    """

    meal_id: str = Field(..., alias="mealId", description="Meal ID")
    school_code: str = Field(..., alias="schoolCode", description="School code")
    school_name: str = Field(..., alias="schoolName", description="School name")
    office_code: str = Field(..., alias="officeCode", description="Education office code")
    office_name: str = Field(..., alias="officeName", description="Education office name")
    meal_date: date = Field(..., alias="mealDate", description="Meal date")
    meal_type: MealType = Field(..., alias="mealType", description="Meal type")
    meal_menu: list[str] = Field(
        default_factory=list, alias="mealMenu", description="Menu items"
    )
    meal_allergy_info: list[str] = Field(
        default_factory=list, alias="mealAllergyInfo", description="Allergy information"
    )
    meal_calories: Optional[str] = Field(None, alias="mealCalories", description="Calories")
    origin_info: Optional[str] = Field(
        None, alias="originInfo", description="Origin of ingredients"
    )
    nutrition_info: Optional[str] = Field(
        None, alias="nutritionInfo", description="Nutrition information"
    )
    meal_serve_count: Optional[int] = Field(
        None, alias="mealServeCount", description="Number of servings"
    )

    model_config = ConfigDict(populate_by_name=True)


class MealResponse(BaseModel):
    """급식 목록 응답 래퍼 (Meal List Response Wrapper).

    Attributes:
        meals: List of meal information
    """

    meals: list[Meal] = Field(default_factory=list, description="List of meals")

    model_config = ConfigDict(populate_by_name=True)


class Schedule(BaseModel):
    """학사일정 정보 (School Schedule Information).

    Information about school academic schedules from NEIS.

    Attributes:
        schedule_id: Schedule ID
        school_code: School code
        school_name: School name
        office_code: Education office code
        office_name: Education office name
        schedule_date: Schedule date
        academic_year: Academic year
        event_name: Event name
        event_content: Event content/description
        day_category: Day category
        school_course_type: School course type
        day_night_type: Day/night type
        target_grades: Target grades for the event
    """

    schedule_id: str = Field(..., alias="scheduleId", description="Schedule ID")
    school_code: str = Field(..., alias="schoolCode", description="School code")
    school_name: str = Field(..., alias="schoolName", description="School name")
    office_code: str = Field(..., alias="officeCode", description="Education office code")
    office_name: str = Field(..., alias="officeName", description="Education office name")
    schedule_date: date = Field(..., alias="scheduleDate", description="Schedule date")
    academic_year: Optional[str] = Field(None, alias="academicYear", description="Academic year")
    event_name: Optional[str] = Field(None, alias="eventName", description="Event name")
    event_content: Optional[str] = Field(
        None, alias="eventContent", description="Event description"
    )
    day_category: Optional[str] = Field(None, alias="dayCategory", description="Day category")
    school_course_type: Optional[str] = Field(
        None, alias="schoolCourseType", description="School course type"
    )
    day_night_type: Optional[str] = Field(
        None, alias="dayNightType", description="Day/night type"
    )
    target_grades: list[int] = Field(
        default_factory=list, alias="targetGrades", description="Target grades"
    )

    model_config = ConfigDict(populate_by_name=True)


class ScheduleResponse(BaseModel):
    """학사일정 목록 응답 래퍼 (Schedule List Response Wrapper).

    Attributes:
        schedules: List of schedule information
    """

    schedules: list[Schedule] = Field(default_factory=list, description="List of schedules")

    model_config = ConfigDict(populate_by_name=True)


class Timetable(BaseModel):
    """시간표 정보 (Timetable Information).

    Information about school timetables from NEIS.

    Attributes:
        timetable_id: Timetable ID
        school_code: School code
        school_name: School name
        office_code: Education office code
        office_name: Education office name
        timetable_date: Timetable date
        academic_year: Academic year
        semester: Semester (nullable)
        grade: Grade (1-3)
        class_num: Class number (1-4)
        period: Period number
        subject: Subject name (nullable)
    """

    timetable_id: str = Field(..., alias="timetableId", description="Timetable ID")
    school_code: str = Field(..., alias="schoolCode", description="School code")
    school_name: str = Field(..., alias="schoolName", description="School name")
    office_code: str = Field(..., alias="officeCode", description="Education office code")
    office_name: str = Field(..., alias="officeName", description="Education office name")
    timetable_date: date = Field(..., alias="timetableDate", description="Timetable date")
    academic_year: str = Field(..., alias="academicYear", description="Academic year")
    semester: Optional[str] = Field(None, alias="semester", description="Semester")
    grade: int = Field(..., alias="grade", description="Grade (1-3)")
    class_num: int = Field(..., alias="classNum", description="Class number (1-4)")
    period: int = Field(..., alias="period", description="Period number")
    subject: Optional[str] = Field(None, alias="subject", description="Subject name")

    model_config = ConfigDict(populate_by_name=True)


class TimetableResponse(BaseModel):
    """시간표 목록 응답 래퍼 (Timetable List Response Wrapper).

    Attributes:
        timetables: List of timetable information
    """

    timetables: list[Timetable] = Field(default_factory=list, description="List of timetables")

    model_config = ConfigDict(populate_by_name=True)
