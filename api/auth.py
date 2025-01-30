from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from api.config import settings

api_key_header = APIKeyHeader(name="X-API-Key")


async def verify_api_key(api_key: str = Depends(api_key_header)):
    """Verify the API key for admin endpoints"""
    if api_key != settings.admin_api_key:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key",
        )
    return api_key
