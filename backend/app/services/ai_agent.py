from typing import Dict, Any
from openai import AsyncOpenAI
from ..core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def get_personalized_recommendations(
    recommendation_type: str, context: Dict[str, Any]
) -> Dict[str, Any]:
    """Get personalized recommendations using AI."""

    prompts = {
        "zodiac_sign": """
        Based on the birth date {birth_date}, provide detailed zodiac sign 
        information. Include specific personality traits, strengths, and areas 
        for growth. Format the response as a JSON with name, symbol, element, 
        and date_range.
        """,
        "date_recommendations": """
        For someone with Life Path Number {numerology_number} and zodiac sign 
        {zodiac_sign} ({element}), analyze these dates: {dates}.
        
        For each date, provide:
        1. The most auspicious category (career/personal/rest/financial)
        2. Optimal timing for activities
        3. Power level (1-3)
        4. Specific, personalized activities based on their zodiac and 
            numerology
        
        Consider astrological aspects, numerological significance, and element 
        compatibility.
        Format as a JSON with date-keyed recommendations.
        """,
        "power_periods": """
        Analyze these dates: {dates}
        For someone with {zodiac_element} element and Life Path 
        {numerology_number},
        identify powerful date clusters where energy alignment is strongest.
        
        Consider:
        - Elemental compatibility
        - Numerological resonance
        - Astrological aspects
        
        Format as a JSON array of power periods with start_date, end_date, dates, and duration.
        """,
    }

    prompt = prompts[recommendation_type].format(**context)

    response = await client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert astrologer and numerologist "
                    "specializing in personalized date recommendations."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content
