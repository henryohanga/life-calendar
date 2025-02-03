from datetime import datetime
from typing import Dict, Any


def get_zodiac_sign(birth_date: str) -> Dict[str, Any]:
    """Calculate zodiac sign and its characteristics from birth date."""
    date = datetime.strptime(birth_date, "%Y-%m-%d")
    month = date.month
    day = date.day

    # Basic zodiac sign data - recommendations will come from AI
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return {
            "name": "Aries",
            "symbol": "♈",
            "element": "Fire",
            "date_range": "March 21 - April 19",
        }
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return {
            "name": "Taurus",
            "symbol": "♉",
            "element": "Earth",
            "date_range": "April 20 - May 20",
        }
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return {
            "name": "Gemini",
            "symbol": "♊",
            "element": "Air",
            "date_range": "May 21 - June 20",
        }
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return {
            "name": "Cancer",
            "symbol": "♋",
            "element": "Water",
            "date_range": "June 21 - July 22",
        }
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return {
            "name": "Leo",
            "symbol": "♌",
            "element": "Fire",
            "date_range": "July 23 - August 22",
        }
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return {
            "name": "Virgo",
            "symbol": "♍",
            "element": "Earth",
            "date_range": "August 23 - September 22",
        }
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return {
            "name": "Libra",
            "symbol": "♎",
            "element": "Air",
            "date_range": "September 23 - October 22",
        }
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return {
            "name": "Scorpio",
            "symbol": "♏",
            "element": "Water",
            "date_range": "October 23 - November 21",
        }
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return {
            "name": "Sagittarius",
            "symbol": "♐",
            "element": "Fire",
            "date_range": "November 22 - December 21",
        }
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return {
            "name": "Capricorn",
            "symbol": "♑",
            "element": "Earth",
            "date_range": "December 22 - January 19",
        }
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return {
            "name": "Aquarius",
            "symbol": "♒",
            "element": "Air",
            "date_range": "January 20 - February 18",
        }
    else:  # Pisces (February 19 - March 20)
        return {
            "name": "Pisces",
            "symbol": "♓",
            "element": "Water",
            "date_range": "February 19 - March 20",
        }
