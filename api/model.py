from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from api.docs import GOOD_DATES_EXAMPLE


class GoodDateRequest(BaseModel):
    birth_date: str = Field(
        ...,
        description="Birth date in YYYY-MM-DD format",
        example="1990-01-01",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
    )
    match_on_single_digit: bool = Field(
        default=True, description="Whether to reduce numbers to a single digit"
    )
    year: Optional[int] = Field(
        default=None,
        description="Year to find dates for (defaults to current year)",
        ge=1900,
        le=2100,
    )

    @validator("birth_date")
    def validate_birth_date(cls, v):
        try:
            year, month, day = map(int, v.split("-"))
            date(year, month, day)
            return v
        except (ValueError, TypeError):
            raise ValueError("Invalid birth date format. Use YYYY-MM-DD")

    class Config:
        schema_extra = {
            "example": {
                "birth_date": "1990-01-01",
                "match_on_single_digit": True,
                "year": 2024,
            }
        }


class GoodDateResponse(BaseModel):
    dates: List[str] = Field(
        ...,
        description="List of dates that match your numerology number",
        example=["2024-01-01", "2024-01-10", "2024-01-19"],
    )
    numerology_number: int = Field(
        ..., description="Your numerology number", example=7, ge=1, le=9
    )
    number_meaning: str = Field(
        ...,
        description="The meaning of your numerology number",
        example="Analysis, spirituality, and wisdom",
    )
    total_matches: int = Field(
        ..., description="Total number of matching dates found", example=36
    )

    class Config:
        json_schema_extra = {"example": GOOD_DATES_EXAMPLE}
