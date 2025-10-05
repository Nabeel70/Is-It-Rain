"""Rate limiting middleware for API protection."""

from __future__ import annotations

import time
from collections import defaultdict
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""

    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
    ) -> None:
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.minute_requests: dict[str, list[float]] = defaultdict(list)
        self.hour_requests: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check rate limits before processing request."""
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # Clean old entries
        self._clean_old_entries(client_ip, current_time)

        # Check minute limit
        if len(self.minute_requests[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": f"Rate limit exceeded: {self.requests_per_minute} requests per minute"
                },
                headers={"Retry-After": "60"},
            )

        # Check hour limit
        if len(self.hour_requests[client_ip]) >= self.requests_per_hour:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": f"Rate limit exceeded: {self.requests_per_hour} requests per hour"
                },
                headers={"Retry-After": "3600"},
            )

        # Add current request
        self.minute_requests[client_ip].append(current_time)
        self.hour_requests[client_ip].append(current_time)

        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Minute-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Minute-Remaining"] = str(
            self.requests_per_minute - len(self.minute_requests[client_ip])
        )
        response.headers["X-RateLimit-Hour-Limit"] = str(self.requests_per_hour)
        response.headers["X-RateLimit-Hour-Remaining"] = str(
            self.requests_per_hour - len(self.hour_requests[client_ip])
        )

        return response

    def _clean_old_entries(self, client_ip: str, current_time: float) -> None:
        """Remove entries older than the time windows."""
        minute_ago = current_time - 60
        hour_ago = current_time - 3600

        self.minute_requests[client_ip] = [
            t for t in self.minute_requests[client_ip] if t > minute_ago
        ]
        self.hour_requests[client_ip] = [
            t for t in self.hour_requests[client_ip] if t > hour_ago
        ]
