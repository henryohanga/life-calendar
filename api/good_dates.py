from typing import List, Tuple
import calendar
from api.numerology import (
    get_date_compatibility,
    get_number_meaning,
    calculate_life_path_number,
)


def good_dates(
    year: int,
    birth_date: str,
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
