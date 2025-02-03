from typing import Dict, Any
import json
from ..schemas.zodiac import GoodDateResponse, ZodiacSign, DateAdvice, PowerPeriod
from datetime import datetime
from ..services.ai_agent import get_personalized_recommendations


async def get_zodiac_sign(birth_date: str) -> Dict[str, Any]:
    """Get zodiac sign information based on birth date."""
    # Get zodiac sign details using birth date
    zodiac_details = await get_personalized_recommendations(
        "zodiac_sign", {"birth_date": birth_date}
    )
    return zodiac_details


async def get_date_recommendations(
    dates: list[str], zodiac_sign: Dict[str, Any]
) -> Dict[str, Dict[str, Any]]:
    """Get recommendations for specific dates."""
    # Get personalized recommendations for each date
    recommendations = await get_personalized_recommendations(
        "date_recommendations",
        {
            "dates": dates,
            "context": {
                "numerology_number": 4,  # Will be replaced with actual calculation
                "zodiac_sign": zodiac_sign["name"],
                "element": zodiac_sign["element"],
            },
        },
    )
    return recommendations


async def get_power_periods(
    dates: list[str], zodiac_sign: Dict[str, Any]
) -> list[Dict[str, Any]]:
    """Calculate power periods from given dates."""
    # Get AI-powered power period recommendations
    power_periods = await get_personalized_recommendations(
        "power_periods",
        {
            "dates": dates,
            "zodiac_element": zodiac_sign["element"],
            "numerology_number": 4,  # Will be replaced with actual calculation
        },
    )
    return power_periods


def format_zodiac_response(zodiac_data: Dict[str, Any]) -> Dict[str, Any]:
    zodiac_sign = ZodiacSign(
        name=zodiac_data["name"],
        symbol=zodiac_data["symbol"],
        element=zodiac_data["element"],
        date_range=zodiac_data["date_range"],
        recommendations={
            "career": zodiac_data.get("recommendations", {}).get("career", []),
            "personal": zodiac_data.get("recommendations", {}).get("personal", []),
            "rest": zodiac_data.get("recommendations", {}).get("rest", []),
            "financial": zodiac_data.get("recommendations", {}).get("financial", []),
            "power_periods": zodiac_data.get("recommendations", {}).get(
                "power_periods", []
            ),
            "date_specific_advice": zodiac_data.get("recommendations", {}).get(
                "date_specific_advice", {}
            ),
        },
    )

    return zodiac_sign.model_dump()


async def get_zodiac_recommendations(
    birth_date: str, dates: list[str]
) -> Dict[str, Any]:
    """Get zodiac sign recommendations for given dates."""
    # Get zodiac sign for birth date
    zodiac_sign = await get_zodiac_sign(birth_date)
    zodiac_sign = json.loads(zodiac_sign)  # Parse JSON string

    # Get recommendations for dates
    date_advice = await get_date_recommendations(dates, zodiac_sign)
    date_advice = json.loads(date_advice)  # Parse JSON string

    # Get recommendations by category
    recommendations = {
        "career": [
            "Use your Life Path energy for career advancement",
            "Focus on leadership and initiative during power periods",
            "Schedule important meetings during high-energy dates",
        ],
        "personal": [
            f"Align personal goals with {zodiac_sign['name']}'s natural strengths",
            "Use power dates for important personal decisions",
            "Focus on relationships during harmonious periods",
        ],
        "rest": [
            "Take advantage of natural energy dips for rejuvenation",
            "Plan vacations during favorable date clusters",
            "Use quiet periods for reflection and planning",
        ],
        "financial": [
            "Make major financial decisions on power dates",
            "Plan investments during auspicious periods",
            "Review finances during clear-minded phases",
        ],
        "power_periods": await get_power_periods(dates, zodiac_sign),
        "date_specific_advice": date_advice,
    }

    # Your existing logic to get zodiac data
    zodiac_data = {
        "name": zodiac_sign["name"],
        "symbol": zodiac_sign["symbol"],
        "element": zodiac_sign["element"],
        "date_range": zodiac_sign["date_range"],
        "recommendations": recommendations,
    }

    # Format the response using the new schema
    formatted_zodiac = format_zodiac_response(zodiac_data)

    response = GoodDateResponse(
        numerology_number=4,  # Replace with actual calculation
        number_meaning="Stability, organization, and hard work",  # Replace with actual meaning
        zodiac_sign=formatted_zodiac,
    )

    return response.model_dump()
