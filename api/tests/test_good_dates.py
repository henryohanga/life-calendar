import pytest
from typing import List
from api.good_dates import good_dates


@pytest.mark.parametrize(
    "year,birth_date,match_on_single_digit,expected_count",
    [
        (2024, "1990-01-01", True, 40),  # Approximate count
        (2024, "2000-12-31", True, 40),
        (2024, "1955-11-11", False, 12),
    ],
)
def test_good_dates(
    year: int,
    birth_date: str,
    match_on_single_digit: bool,
    expected_count: int,
) -> None:
    """
    Test good dates calculation with various inputs.

    Args:
        year: Year to find dates for
        birth_date: Birth date in YYYY-MM-DD format
        match_on_single_digit: Whether to reduce numbers to single digit
        expected_count: Expected number of matching dates

    Verifies:
        - Return types and formats
        - Date string formatting
        - Approximate count of matching dates
    """
    dates: List[str]
    number: int
    meaning: str
    dates, number, meaning = good_dates(year, birth_date, match_on_single_digit)

    # Check return types
    assert isinstance(dates, list)
    assert all(isinstance(d, str) for d in dates)
    assert isinstance(number, int)
    assert isinstance(meaning, str)

    # Check date format
    assert all(d.startswith(f"{year}-") for d in dates)
    assert all(len(d) == 10 for d in dates)  # YYYY-MM-DD

    # Check approximate count (may vary by year)
    assert abs(len(dates) - expected_count) < 10


def test_good_dates_invalid_input() -> None:
    """Test error handling for invalid date input."""
    with pytest.raises(ValueError):
        good_dates(2024, "invalid-date", True)
