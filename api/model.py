from datetime import date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from api.docs import GOOD_DATES_EXAMPLE


class GoodDateRequest(BaseModel):
    birth_date: str = Field(
        ...,
        description="Birth date in YYYY-MM-DD format",
        example="1990-01-01",
    )
    match_on_single_digit: bool = Field(
        True,
        description="Whether to match on single digit numerology",
    )
    year: Optional[int] = Field(
        None,
        description="Year to calculate dates for (defaults to current year)",
    )
    include_zodiac: bool = Field(
        False,
        description="Whether to include zodiac sign information",
    )

    @validator("birth_date")
    def validate_birth_date(cls, v):
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("birth_date must be in YYYY-MM-DD format")

    class Config:
        schema_extra = {
            "example": {
                "birth_date": "1990-01-01",
                "match_on_single_digit": True,
                "year": 2024,
                "include_zodiac": False,
            }
        }


class GoodDateResponse(BaseModel):
    dates: List[str] = Field(
        ...,
        description="List of good dates",
        example=["2024-01-01", "2024-01-10"],
    )
    numerology_number: int = Field(
        ...,
        description="Your numerology number",
        example=7,
    )
    number_meaning: str = Field(
        ...,
        description="The meaning of your numerology number",
        example="Analysis, spirituality, and wisdom",
    )
    total_matches: int = Field(
        ...,
        description="Total number of matching dates found",
        example=36,
    )
    zodiac_sign: Optional[Dict[str, Any]] = Field(
        None,
        description="Zodiac sign information and recommendations",
    )

    class Config:
        json_schema_extra = {"example": GOOD_DATES_EXAMPLE}
