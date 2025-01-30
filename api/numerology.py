from typing import Tuple


def calculate_life_path_number(birth_date: str, single_digit: bool = True) -> int:
    """Calculate life path number from birth date"""
    # Remove hyphens and convert to integers
    numbers = [int(n) for n in birth_date.replace("-", "")]

    # Sum all digits
    total = sum(numbers)

    if single_digit and total > 9:
        # Keep reducing until we get a single digit
        while total > 9:
            total = sum(int(d) for d in str(total))

    return total


def calculate_date_number(date_str: str, single_digit: bool = True) -> int:
    """Calculate numerology number for a specific date"""
    # Same logic as life path number
    return calculate_life_path_number(date_str, single_digit)


def get_date_compatibility(
    birth_date: str, target_date: str, single_digit: bool = True
) -> Tuple[bool, int, int]:
    """
    Calculate compatibility between birth date and target date.
    Returns (is_compatible, birth_number, date_number)
    """
    birth_number = calculate_life_path_number(birth_date, single_digit)
    date_number = calculate_date_number(target_date, single_digit)

    return date_number == birth_number, birth_number, date_number


def get_number_meaning(number: int) -> str:
    """Get the meaning of a numerology number"""
    meanings = {
        1: "Leadership, independence, and new beginnings",
        2: "Harmony, partnership, and diplomacy",
        3: "Creativity, communication, and self-expression",
        4: "Stability, organization, and hard work",
        5: "Freedom, change, and adventure",
        6: "Nurturing, responsibility, and love",
        7: "Analysis, spirituality, and wisdom",
        8: "Power, abundance, and achievement",
        9: "Compassion, completion, and universal love",
    }
    return meanings.get(number, "Unknown number meaning")
