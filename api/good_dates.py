from typing import List, Tuple, Dict, Any
import calendar
from api.numerology import (
    get_date_compatibility,
    get_number_meaning,
    calculate_life_path_number,
)
from api.zodiac import get_zodiac_sign
from api.ai_recommendations import get_personalized_recommendations


def calculate_numerology_dates(
    birth_date: str,
    year: int,
    match_on_single_digit: bool = True,
) -> Tuple[List[str], int, str]:
    """Calculate good dates based on numerology."""
    # Get initial numerology number for birth date
    birth_number = calculate_life_path_number(birth_date, match_on_single_digit)

    dates = []
    for month in range(1, 13):
        for day in range(1, calendar.monthrange(int(year), month)[1] + 1):
            date = f"{year}-{month:02}-{day:02}"
            is_compatible, _, _ = get_date_compatibility(
                birth_date=birth_date,
                target_date=date,
                single_digit=match_on_single_digit,
            )
            if is_compatible:
                dates.append(date)

    meaning = get_number_meaning(birth_number)
    return dates, birth_number, meaning


def calculate_zodiac_favorable_dates(
    zodiac_info: Dict[str, Any], year: int
) -> List[str]:
    """Calculate favorable dates based on zodiac sign."""
    # This is a placeholder - we'll implement actual zodiac calculations later
    return []


async def good_dates(
    birth_date: str,
    year: int,
    match_on_single_digit: bool = True,
    include_zodiac: bool = False,
) -> Tuple[List[str], int, str, Dict[str, Any]]:
    """Calculate good dates based on numerology and zodiac sign."""
    dates, numerology_number, meaning = calculate_numerology_dates(
        birth_date, year, match_on_single_digit
    )

    zodiac_info = None
    if include_zodiac:
        zodiac_info = get_zodiac_sign(birth_date)
        zodiac_info["favorable_dates"] = calculate_zodiac_favorable_dates(
            zodiac_info, year
        )

        # Get AI-powered recommendations
        recommendations = await get_personalized_recommendations(
            numerology_number=numerology_number,
            zodiac_sign=zodiac_info["name"],
            dates=dates,
        )
        zodiac_info["recommendations"] = recommendations

    return dates, numerology_number, meaning, zodiac_info
