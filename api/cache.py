from typing import List, Tuple, Dict, Any
from datetime import datetime, timedelta

from api.good_dates import good_dates as calculate_good_dates

# Cache structure: {key: (result, timestamp)}
_cache: Dict[str, Tuple[Tuple[List[str], int, str, Dict[str, Any]], float]] = {}
CACHE_DURATION = timedelta(hours=24)


def _make_cache_key(
    birth_date: str, year: int, match_on_single_digit: bool, include_zodiac: bool
) -> str:
    """Create a unique cache key."""
    return f"{birth_date}:{year}:{match_on_single_digit}:{include_zodiac}"


async def get_cached_good_dates(
    birth_date: str,
    year: int,
    match_on_single_digit: bool,
    include_zodiac: bool = False,
) -> Tuple[List[str], int, str, Dict[str, Any]]:
    """Get cached good dates calculation results."""
    cache_key = _make_cache_key(birth_date, year, match_on_single_digit, include_zodiac)
    now = datetime.now().timestamp()

    # Check if we have a valid cached result
    if cache_key in _cache:
        result, timestamp = _cache[cache_key]
        if now - timestamp < CACHE_DURATION.total_seconds():
            return result

    # Calculate new result
    result = await calculate_good_dates(
        birth_date=birth_date,
        year=year,
        match_on_single_digit=match_on_single_digit,
        include_zodiac=include_zodiac,
    )

    # Cache the result
    _cache[cache_key] = (result, now)
    return result


def clear_expired_cache() -> None:
    """Clear expired cache entries."""
    now = datetime.now().timestamp()
    expired_keys = [
        key
        for key, (_, timestamp) in _cache.items()
        if now - timestamp >= CACHE_DURATION.total_seconds()
    ]
    for key in expired_keys:
        del _cache[key]
