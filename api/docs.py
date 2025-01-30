from typing import Dict, Any

# Example responses for documentation
GOOD_DATES_EXAMPLE: Dict[str, Any] = {
    "dates": [
        "2024-01-01",
        "2024-01-10",
        "2024-01-19",
        "2024-01-28",
    ],
    "numerology_number": 7,
    "number_meaning": "Analysis, spirituality, and wisdom",
    "total_matches": 36,
}

# API operation descriptions
GOOD_DATES_DESCRIPTION = """
Find dates that align with your numerology based on your birth date.

The endpoint calculates your life path number from your birth date and finds dates
in the specified year that match this number. You can choose whether to reduce
numbers to a single digit (e.g., 28 -> 2+8 -> 10 -> 1).

Example:
- Birth date: 1990-01-01 reduces to 3 (1+9+9+0+0+1+0+1 = 21 -> 2+1 = 3)
- The API will find all dates in the specified year that also reduce to 3

The response includes:
- A list of matching dates
- Your numerology number
- The meaning of your number
- Total count of matches
"""

CACHE_CLEAR_DESCRIPTION = """
Clear the calculation cache.

This endpoint requires admin authentication using an API key in the X-API-Key header.
Use this endpoint to clear cached results if you need to force recalculation.
"""
