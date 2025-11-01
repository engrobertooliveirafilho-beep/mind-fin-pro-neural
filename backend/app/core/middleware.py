from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from app.core.config import settings

try:
    import redis  # opcional
except Exception:
    redis = None

class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._r = None
        if settings.REDIS_URL and redis:
            try:
                self._r = redis.from_url(
                    settings.REDIS_URL,
                    socket_timeout=0.2,
                    socket_connect_timeout=0.2,
                    decode_responses=True
                )
            except Exception:
                self._r = None

    async def dispatch(self, request: Request, call_next):
        # nunca bloqueia health
        if request.url.path == "/health":
            return await call_next(request)

        # sem redis -> segue
        if not self._r:
            return await call_next(request)

        key = f"rl:{request.client.host}"
        try:
            used = self._r.incr(key)
            if used == 1:
                self._r.expire(key, 1)
            if used > 1000:
                return JSONResponse({"detail": "Too many requests"}, status_code=429)
        except Exception:
            # qualquer falha -> fail-open
            return await call_next(request)

        return await call_next(request)
