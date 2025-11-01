from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import Response
from time import perf_counter
import json, uuid
from datetime import datetime
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        start = perf_counter()
        response: Response = await call_next(request)
        latency_ms = int((perf_counter() - start) * 1000)
        response.headers["X-Request-ID"] = rid
        # log simples estruturado
        try:
            user_id = getattr(getattr(request, "state", object()), "user_id", "-")
        except Exception:
            user_id = "-"
        print(json.dumps({
            "ts": datetime.utcnow().isoformat() + "Z",
            "level": "INFO",
            "path": request.url.path,
            "status": response.status_code,
            "latency_ms": latency_ms,
            "request_id": rid,
            "user_id": user_id
        }))
        return response
