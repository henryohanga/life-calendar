import pytest
from api.numerology import (
    calculate_life_path_number,
    get_date_compatibility,
    get_number_meaning,
)


@pytest.mark.parametrize(
    "birth_date,single_digit,expected",
    [
        ("1990-01-01", True, 3),  # 1+9+9+0+0+1+0+1 = 21 -> 2+1 = 3
        ("1990-01-01", False, 21),
        ("2000-12-31", True, 8),  # 2+0+0+0+1+2+3+1 = 9
        ("1955-11-11", True, 7),  # 1+9+5+5+1+1+1+1 = 24 -> 2+4 = 6
    ],
)
def test_calculate_life_path_number(
    birth_date: str, single_digit: bool, expected: int
) -> None:
    """Test life path number calculation with various birth dates."""
    result = calculate_life_path_number(birth_date, single_digit)
    assert result == expected


@pytest.mark.parametrize(
    "birth_date,target_date,single_digit,expected",
    [
        ("1990-01-01", "2024-01-01", True, (True, 3, 3)),
        ("1990-01-01", "2024-01-02", True, (False, 3, 4)),
        ("2000-12-31", "2024-08-17", True, (True, 8, 8)),
    ],
)
def test_get_date_compatibility(
    birth_date: str,
    target_date: str,
    single_digit: bool,
    expected: tuple,
):
    result = get_date_compatibility(birth_date, target_date, single_digit)
    assert result == expected


def test_get_number_meaning() -> None:
    """Test numerology number meanings for valid and invalid numbers."""
    # Test all valid numbers
    for i in range(1, 10):
        meaning = get_number_meaning(i)
        assert isinstance(meaning, str)
        assert len(meaning) > 0
        assert meaning != "Unknown number meaning"

    # Test invalid number
    assert get_number_meaning(10) == "Unknown number meaning"
