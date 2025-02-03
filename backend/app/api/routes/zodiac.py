from fastapi import APIRouter, HTTPException
from typing import List
from ...services.zodiac_service import get_zodiac_recommendations
from ...schemas.zodiac import GoodDateResponse

router = APIRouter()


@router.post("/recommendations", response_model=GoodDateResponse)
async def get_zodiac_date_recommendations(
    birth_date: str, dates: List[str]
) -> GoodDateResponse:
    """Get zodiac sign recommendations for specific dates."""
    try:
        # Using the new service function with proper response model
        recommendations = await get_zodiac_recommendations(birth_date, dates)
        return GoodDateResponse(**recommendations)
    except Exception as e:
        error_msg = f"Error getting zodiac recommendations: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg)
