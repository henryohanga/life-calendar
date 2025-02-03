from typing import List, Dict, Any
import openai
from datetime import datetime
from api.config import settings

# Configure OpenAI
openai.api_key = settings.openai_api_key


def parse_ai_response(content: str) -> Dict[str, List[str]]:
    """Parse the AI response into structured recommendations."""
    try:
        sections = content.split("\n\n")
        activities = []
        timing = []

        for section in sections:
            lines = [
                line.strip("- ").strip()
                for line in section.split("\n")
                if line.strip().startswith("-")
            ]

            # More intelligent section detection
            if any(
                keyword in section.lower()
                for keyword in ["activities", "decisions", "focus", "opportunities"]
            ):
                activities.extend(lines)
            elif any(
                keyword in section.lower()
                for keyword in ["timing", "periods", "windows", "when"]
            ):
                timing.extend(lines)

        # Ensure we get the most impactful recommendations
        activities = [rec for rec in activities if len(rec) > 20][:3]
        timing = [rec for rec in timing if len(rec) > 20][:3]

        return {
            "activities": activities,
            "timing": timing,
        }
    except Exception:
        return get_fallback_recommendations()


def get_fallback_recommendations(
    numerology_number: int = 1, zodiac_sign: str = "Aries"
) -> Dict[str, List[str]]:
    """Provide thoughtful fallback recommendations if AI fails."""
    # More detailed fallback recommendations based on numerology
    numerology_activities = {
        1: [
            "Initiate major projects during high-energy periods",
            "Schedule leadership activities in morning hours",
            "Plan strategic moves during favorable dates",
        ],
        2: [
            "Focus on partnership discussions during harmonious periods",
            "Schedule collaborative projects on balanced days",
            "Plan relationship-building activities during receptive phases",
        ],
        3: [
            "Schedule creative work during peak inspiration times",
            "Plan social events during high-energy dates",
            "Focus on communication projects during mental clarity periods",
        ],
        4: [
            "Structure major organizational tasks during stable periods",
            "Plan foundation-setting activities during grounded phases",
            "Schedule important meetings during practical windows",
        ],
        5: [
            "Plan travel during adventure-favorable dates",
            "Schedule learning activities during expansive periods",
            "Focus on changes during transformative phases",
        ],
        6: [
            "Schedule family events during harmonious periods",
            "Plan nurturing activities during supportive phases",
            "Focus on home improvements during stable windows",
        ],
        7: [
            "Schedule research during contemplative periods",
            "Plan spiritual activities during introspective phases",
            "Focus on analysis during clear-minded windows",
        ],
        8: [
            "Plan business moves during power periods",
            "Schedule financial decisions during prosperous phases",
            "Focus on advancement during ambitious windows",
        ],
        9: [
            "Schedule humanitarian work during service-oriented periods",
            "Plan completion activities during culmination phases",
            "Focus on giving during generous windows",
        ],
    }

    timing = [
        f"Optimal decision-making windows align with {zodiac_sign}'s favorable periods",
        "Schedule rest during natural energy dips in afternoon",
        "Plan major moves during high-energy morning hours",
    ]

    return {
        "activities": numerology_activities.get(
            numerology_number, numerology_activities[1]
        ),
        "timing": timing,
    }


async def get_personalized_recommendations(
    numerology_number: int, zodiac_sign: str, dates: List[str]
) -> Dict[str, Any]:
    """Get AI-powered recommendations with specific dates and times for life events."""
    current_month = datetime.now().month
    prompt = f"""
    As an elite astrologer and numerologist, provide detailed timing analysis for major life decisions:

    PROFILE:
    - Life Path Number: {numerology_number} (core life purpose)
    - Zodiac Sign: {zodiac_sign} (energy patterns)
    - Favorable Dates Available: {', '.join(dates[:8])}
    - Current Month: {current_month} (for seasonal context)

    TASK:
    Analyze these dates and provide highly specific recommendations for optimal timing of important life events.

    PROVIDE RECOMMENDATIONS IN THESE CATEGORIES:

    1. CAREER & BUSINESS
    - Best dates for job interviews, negotiations, or business launches
    - Optimal times for important meetings or presentations
    - Strategic windows for career transitions

    2. PERSONAL DEVELOPMENT & RELATIONSHIPS
    - Prime dates for important personal decisions
    - Optimal periods for relationship discussions
    - Best times for starting new personal projects

    3. REST & REJUVENATION
    - Identify ideal vacation periods
    - Suggest rest day clusters
    - Mark dates for personal retreats

    4. FINANCIAL & LEGAL MATTERS
    - Optimal dates for investments
    - Best timing for contracts or agreements
    - Strategic financial planning windows

    FORMAT REQUIREMENTS:
    - Group recommendations by the favorable dates provided
    - Include specific times of day when applicable
    - Explain why certain dates are particularly powerful
    - Note date clusters that create especially potent periods
    - Highlight any dates that align with zodiac transitions or numerological power days

    Focus on actionable specifics. Combine numerological power days with zodiac energy patterns
    to identify the most auspicious timing for each type of activity.
    """

    try:
        response = await openai.ChatCompletion.acreate(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an elite astrologer and numerologist specializing in precise "
                        "timing optimization. Your expertise lies in identifying exact dates "
                        "and times for important life events by combining numerological power "
                        "days with astrological alignments. Focus on specific dates and times, "
                        "not general advice. Help people plan their calendar for maximum success."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=settings.openai_max_tokens,
            temperature=settings.openai_temperature,
        )

        return parse_enhanced_ai_response(response.choices[0].message.content, dates)
    except Exception:  # pylint: disable=broad-except
        return get_enhanced_fallback_recommendations(
            numerology_number, zodiac_sign, dates
        )


def parse_enhanced_ai_response(
    content: str, available_dates: List[str]
) -> Dict[str, Any]:
    """Parse AI response into structured date-specific recommendations."""
    try:
        sections = content.lower().split("\n\n")
        recommendations = {
            "career": [],
            "personal": [],
            "rest": [],
            "financial": [],
            "power_periods": [],
            "date_specific_advice": {},
        }

        current_category = None
        for section in sections:
            if "career" in section or "business" in section:
                current_category = "career"
            elif "personal" in section or "relationship" in section:
                current_category = "personal"
            elif "rest" in section or "rejuvenation" in section:
                current_category = "rest"
            elif "financial" in section or "legal" in section:
                current_category = "financial"

            # Extract date-specific recommendations
            for date in available_dates:
                if date.lower() in section.lower():
                    date_info = {
                        "activities": [],
                        "timing": None,
                        "power_level": None,
                        "category": current_category,
                    }

                    # Extract time recommendations if present
                    time_indicators = [
                        "morning",
                        "afternoon",
                        "evening",
                        "night",
                        "noon",
                        "dawn",
                        "dusk",
                    ]
                    for indicator in time_indicators:
                        if indicator in section.lower():
                            date_info["timing"] = indicator

                    # Extract the specific recommendation
                    lines = [
                        line.strip("- ").strip()
                        for line in section.split("\n")
                        if line.strip().startswith("-") and len(line) > 20
                    ]
                    date_info["activities"] = lines

                    # Determine power level based on recommendation emphasis
                    power_words = [
                        "powerful",
                        "optimal",
                        "perfect",
                        "ideal",
                        "strongest",
                    ]
                    date_info["power_level"] = sum(
                        1 for word in power_words if word in section.lower()
                    )

                    recommendations["date_specific_advice"][date] = date_info

            # Extract general category recommendations
            if current_category:
                lines = [
                    line.strip("- ").strip()
                    for line in section.split("\n")
                    if line.strip().startswith("-") and len(line) > 20
                ]
                recommendations[current_category].extend(lines)

        # Identify power periods (clusters of high-power dates)
        power_dates = [
            date
            for date, info in recommendations["date_specific_advice"].items()
            if info["power_level"] > 1
        ]
        recommendations["power_periods"] = find_date_clusters(power_dates)

        return recommendations

    except Exception:  # pylint: disable=broad-except
        return get_enhanced_fallback_recommendations(1, "Aries", available_dates)


def find_date_clusters(dates: List[str], max_gap: int = 3) -> List[Dict[str, Any]]:
    """Identify clusters of powerful dates."""
    if not dates:
        return []

    sorted_dates = sorted(dates)
    clusters = []
    current_cluster = [sorted_dates[0]]

    for i in range(1, len(sorted_dates)):
        current_date = datetime.strptime(sorted_dates[i], "%Y-%m-%d")
        prev_date = datetime.strptime(current_cluster[-1], "%Y-%m-%d")

        if (current_date - prev_date).days <= max_gap:
            current_cluster.append(sorted_dates[i])
        else:
            if len(current_cluster) > 1:
                clusters.append(
                    {
                        "start_date": current_cluster[0],
                        "end_date": current_cluster[-1],
                        "dates": current_cluster,
                        "duration": len(current_cluster),
                    }
                )
            current_cluster = [sorted_dates[i]]

    if len(current_cluster) > 1:
        clusters.append(
            {
                "start_date": current_cluster[0],
                "end_date": current_cluster[-1],
                "dates": current_cluster,
                "duration": len(current_cluster),
            }
        )

    return clusters


def get_enhanced_fallback_recommendations(
    numerology_number: int, zodiac_sign: str, dates: List[str]
) -> Dict[str, Any]:
    """Provide detailed fallback recommendations with specific dates."""
    if not dates:
        return {
            "career": [],
            "personal": [],
            "rest": [],
            "financial": [],
            "power_periods": [],
            "date_specific_advice": {},
        }

    # Basic category recommendations based on numerology
    base_recommendations = {
        "career": [
            f"Use your Life Path {numerology_number} energy for career advancement",
            "Focus on leadership and initiative during power periods",
            "Schedule important meetings during high-energy dates",
        ],
        "personal": [
            f"Align personal goals with {zodiac_sign}'s natural strengths",
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
    }

    # Date-specific recommendations
    date_specific_advice = {}
    sorted_dates = sorted(dates)

    # Categorize dates based on their position in the month
    for date in sorted_dates:
        day = int(date.split("-")[2])
        month_position = "early" if day <= 10 else "mid" if day <= 20 else "late"

        date_info = {
            "activities": [],
            "timing": get_optimal_timing(date, zodiac_sign),
            "power_level": calculate_power_level(date, numerology_number),
            "category": get_date_category(date, zodiac_sign),
        }

        # Add specific recommendations based on date characteristics
        date_info["activities"] = get_date_activities(
            date, zodiac_sign, numerology_number, month_position
        )

        date_specific_advice[date] = date_info

    # Find powerful date clusters
    power_dates = [
        date for date, info in date_specific_advice.items() if info["power_level"] > 1
    ]
    power_periods = find_date_clusters(power_dates)

    return {
        "career": base_recommendations["career"],
        "personal": base_recommendations["personal"],
        "rest": base_recommendations["rest"],
        "financial": base_recommendations["financial"],
        "power_periods": power_periods,
        "date_specific_advice": date_specific_advice,
    }


def get_optimal_timing(date: str, zodiac_sign: str) -> str:
    """Determine optimal timing based on zodiac sign and date."""
    zodiac_timings = {
        "Aries": "morning",
        "Taurus": "mid-morning",
        "Gemini": "afternoon",
        "Cancer": "evening",
        "Leo": "noon",
        "Virgo": "morning",
        "Libra": "afternoon",
        "Scorpio": "evening",
        "Sagittarius": "morning",
        "Capricorn": "early morning",
        "Aquarius": "afternoon",
        "Pisces": "evening",
    }
    return zodiac_timings.get(zodiac_sign, "morning")


def calculate_power_level(date: str, numerology_number: int) -> int:
    """Calculate power level based on date numerology."""
    day = int(date.split("-")[2])
    month = int(date.split("-")[1])

    # Calculate date's numerology
    date_number = sum(int(d) for d in str(day + month))
    while date_number > 9:
        date_number = sum(int(d) for d in str(date_number))

    # Higher power level if date numerology matches life path
    base_power = 1
    if date_number == numerology_number:
        base_power += 1
    if day == numerology_number:
        base_power += 1

    return base_power


def get_date_category(date: str, zodiac_sign: str) -> str:
    """Determine best category for a date based on zodiac and timing."""
    day = int(date.split("-")[2])

    # Simplified category assignment based on date patterns
    if day % 4 == 0:
        return "career"
    elif day % 4 == 1:
        return "personal"
    elif day % 4 == 2:
        return "rest"
    else:
        return "financial"


def get_date_activities(
    date: str, zodiac_sign: str, numerology_number: int, month_position: str
) -> List[str]:
    """Generate specific activities for a date based on all factors."""
    activities = []
    day = int(date.split("-")[2])

    # Add activities based on numerology
    if day % numerology_number == 0:
        activities.append(
            f"Excellent day for {zodiac_sign}-aligned projects requiring focus and determination"
        )

    # Add position-based activities
    position_activities = {
        "early": "Start new initiatives and plan ahead",
        "mid": "Execute ongoing projects and maintain momentum",
        "late": "Complete tasks and reflect on achievements",
    }
    activities.append(position_activities[month_position])

    # Add zodiac-specific activity
    zodiac_activities = {
        "Fire": "Take bold action and lead initiatives",
        "Earth": "Focus on practical and material matters",
        "Air": "Engage in communication and learning",
        "Water": "Focus on emotional and intuitive work",
    }
    element = get_zodiac_element(zodiac_sign)
    activities.append(zodiac_activities[element])

    return activities


def get_zodiac_element(zodiac_sign: str) -> str:
    """Get the element for a zodiac sign."""
    elements = {
        "Aries": "Fire",
        "Leo": "Fire",
        "Sagittarius": "Fire",
        "Taurus": "Earth",
        "Virgo": "Earth",
        "Capricorn": "Earth",
        "Gemini": "Air",
        "Libra": "Air",
        "Aquarius": "Air",
        "Cancer": "Water",
        "Scorpio": "Water",
        "Pisces": "Water",
    }
    return elements.get(zodiac_sign, "Fire")
