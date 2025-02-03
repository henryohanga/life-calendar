from typing import Dict, Any, List
from pydantic import BaseModel


class PowerPeriod(BaseModel):
    start_date: str
    end_date: str
    dates: List[str]
    duration: int


class ZodiacRecommendations(BaseModel):
    career: List[str]
    personal: List[str]
    rest: List[str]
    financial: List[str]
    power_periods: List[PowerPeriod]
    date_specific_advice: Dict[str, Dict[str, Any]]


class ZodiacSign(BaseModel):
    name: str
    symbol: str
    element: str
    date_range: str
    recommendations: ZodiacRecommendations


class GoodDateResponse(BaseModel):
    numerology_number: int
    number_meaning: str
    zodiac_sign: ZodiacSign
