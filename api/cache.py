from functools import lru_cache
from typing import List, Tuple

from api.good_dates import good_dates as calculate_good_dates


@lru_cache(maxsize=1000)
def get_cached_good_dates(
    birth_date: str, year: int, match_on_single_digit: bool
) -> Tuple[List[str], int, str]:
    """
    Calculate and cache good dates for a given birth date and year.
    Returns a tuple of (dates, numerology_number, number_meaning).
    """
    return calculate_good_dates(
        birth_date=birth_date,
        year=year,
        match_on_single_digit=match_on_single_digit,
    )


def clear_expired_cache() -> None:
    """Clear all cached entries"""
    get_cached_good_dates.cache_clear()
