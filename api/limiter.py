from datetime import datetime, timedelta
from typing import Dict, Tuple
from fastapi import HTTPException, Request


class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, Tuple[int, datetime]] = {}

    def is_rate_limited(self, key: str) -> bool:
        now = datetime.now()
        if key not in self.requests:
            self.requests[key] = (1, now)
            return False

        count, timestamp = self.requests[key]
        time_passed = now - timestamp

        if time_passed > timedelta(minutes=1):
            self.requests[key] = (1, now)
            return False

        if count >= self.requests_per_minute:
            return True

        self.requests[key] = (count + 1, timestamp)
        return False


rate_limiter = RateLimiter(requests_per_minute=60)


async def check_rate_limit(request: Request):
    """Dependency to check rate limit based on client IP"""
    client_ip = request.client.host if request.client else "unknown"

    if rate_limiter.is_rate_limited(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again in a minute.",
            headers={"Retry-After": "60"},
        )
