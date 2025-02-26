from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from api.model import GoodDateRequest, GoodDateResponse
from api.cache import get_cached_good_dates, clear_expired_cache
from api.limiter import check_rate_limit
from api.logger import setup_logging, logger
from api.auth import verify_api_key
from api.config import settings
from api.docs import (
    GOOD_DATES_EXAMPLE,
    GOOD_DATES_DESCRIPTION,
    CACHE_CLEAR_DESCRIPTION,
)

app = FastAPI(
    title="Good Dates API",
    description="""
    The Good Dates API helps you find dates that align with your numerology.
    Calculate your life path number and discover dates that resonate with your energy.
    """,
    version="1.0.0",
    contact={
        "name": "Henry Ohanga",
        "email": "ohanga.henry@gmail.com",
        "url": "https://github.com/henryohanga",
    },
)

# Setup logging
setup_logging(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Good Dates API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


@app.post("/good-dates/", response_model=GoodDateResponse)
async def get_good_dates(
    request: GoodDateRequest,
    _rate_limit: None = Depends(check_rate_limit),
) -> GoodDateResponse:
    """Get good dates based on numerology and zodiac sign."""
    try:
        logger.info(
            f"Calculating good dates for birth_date={request.birth_date}, year={request.year}"
        )

        dates, numerology_number, number_meaning, zodiac_info = (
            await get_cached_good_dates(
                birth_date=request.birth_date,
                year=request.year or datetime.now().year,
                match_on_single_digit=request.match_on_single_digit,
                include_zodiac=request.include_zodiac,
            )
        )

        return GoodDateResponse(
            dates=dates,
            numerology_number=numerology_number,
            number_meaning=number_meaning,
            total_matches=len(dates),
            zodiac_sign=zodiac_info if request.include_zodiac else None,
        )

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@app.post("/cache/clear")
async def clear_cache(
    _rate_limit: None = Depends(check_rate_limit), _auth: str = Depends(verify_api_key)
):
    """Clear the calculation cache."""
    logger.info("Clearing calculation cache")
    clear_expired_cache()
    return {"message": "Cache cleared successfully"}
